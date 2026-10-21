"""Offline schema and evidence integrity validation; no network resolution."""
import hashlib
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator


def validate(root):
    root = Path(root).resolve()
    records = {}
    categories = {}
    for path in sorted((root / 'records').glob('*/*.json')):
        category = path.parent.name
        schema = json.loads((root / 'schemas' / (category + '.schema.json')).read_text())
        Draft202012Validator.check_schema(schema)
        record = json.loads(path.read_text())
        Draft202012Validator(schema).validate(record)
        if record['id'] in records:
            raise ValueError('duplicate record ID: ' + record['id'])
        records[record['id']] = record
        categories[record['id']] = category
    if not records:
        raise ValueError('corpus has no records')

    def reference(id, category):
        if categories.get(id) != category:
            raise ValueError('missing or wrong reference: ' + id + ' (' + category + ')')
        return records[id]

    for id, rec in records.items():
        category = categories[id]
        for key, target in [('sources', 'source'), ('experiments', 'experiment'),
                            ('fixtures', 'fixture'), ('claims', 'claim'),
                            ('conflicts_with', 'claim'), ('supersedes', 'claim')]:
            for value in rec.get(key, []):
                reference(value, target)
                if value == id:
                    raise ValueError('self reference: ' + id)
        if category == 'controller' and rec['parent']:
            reference(rec['parent'], 'controller')
            if rec['parent'] == id:
                raise ValueError('self reference: ' + id)
        if category == 'claim':
            reference(rec['applicability']['controller'], 'controller')
        if category == 'report':
            reference(rec['claim'], 'claim')
        if category == 'claim':
            if rec['status'] != 'unknown' and not rec['sources'] and not rec['experiments']:
                raise ValueError('claim has no provenance: ' + id)
            if rec['status'] == 'rejected' and not rec['rejection_scope']:
                raise ValueError('rejection requires scope: ' + id)
            if rec['status'] == 'conflicted' and not rec['conflicts_with']:
                raise ValueError('conflict requires alternatives: ' + id)
            if rec['status'] == 'independently_corroborated':
                lineages = {reference(s, 'source')['lineage'] for s in rec['sources']}
                if len(lineages) < 2:
                    raise ValueError('independence requires distinct source lineages: ' + id)
            if rec['status'] in ('physically_observed', 'physically_validated'):
                proven = False
                for exp_id in rec['experiments']:
                    exp = reference(exp_id, 'experiment')
                    physical = any(reference(f, 'fixture')['kind'] == 'physical' and id in reference(f, 'fixture')['claims'] for f in exp['fixtures'])
                    if exp['kind'] == 'controlled_physical' and exp['status'] == 'passed' and physical:
                        proven |= bool(exp['semantic_outcome']) or rec['status'] == 'physically_observed'
                if not proven:
                    raise ValueError('physical promotion lacks evidence: ' + id)
        if category == 'fixture':
            relative = Path(rec['path'])
            path = (root / relative).resolve()
            if relative.is_absolute() or not path.is_relative_to(root):
                raise ValueError('fixture escapes corpus: ' + id)
            if hashlib.sha256(path.read_bytes()).hexdigest() != rec['sha256']:
                raise ValueError('fixture hash mismatch: ' + id)
            if rec['format'] == 'hid_report_hex':
                bytes.fromhex(path.read_text().strip())
            elif rec['format'] == 'acceptance_run_json':
                if rec['kind'] != 'virtual_host_run':
                    raise ValueError('acceptance runs require virtual_host_run fixture kind: ' + id)
                run = json.loads(path.read_text())
                schema = json.loads((root / 'schemas/acceptance-run.schema.json').read_text())
                Draft202012Validator.check_schema(schema)
                Draft202012Validator(schema).validate(run)
                if run['environment'].get('synthetic') is not False or run['environment'].get('backend') != 'linux':
                    raise ValueError('virtual host run must be measured Linux backend, not fake: ' + id)
                if not rec['experiments'] or any(reference(exp, 'experiment')['kind'] != 'virtual_host_run' for exp in rec['experiments']):
                    raise ValueError('acceptance run requires virtual-host experiment: ' + id)
            else:
                trace = json.loads(path.read_text())
                if trace.get('manifest', {}).get('synthetic') is not (rec['kind'] == 'synthetic'):
                    raise ValueError('evdev trace synthetic flag disagrees with fixture kind: ' + id)
            if rec['kind'] == 'synthetic' and rec['parent']:
                raise ValueError('synthetic fixture cannot disguise a capture transformation')
            if rec['kind'] == 'sanitized' and (not rec['parent'] or not rec['transform']):
                raise ValueError('sanitized fixture lacks lineage: ' + id)
            if rec['kind'] == 'physical' and not rec['experiments']:
                raise ValueError('physical fixture lacks experiment: ' + id)
            seen = {id}
            parent = rec['parent']
            while parent:
                if parent in seen:
                    raise ValueError('cyclic fixture lineage: ' + id)
                seen.add(parent)
                parent = reference(parent, 'fixture')['parent']
    return len(records)


if __name__ == '__main__':
    try:
        print('Validated', validate(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]), 'records')
    except (ValueError, OSError, KeyError) as error:
        sys.exit(str(error))
