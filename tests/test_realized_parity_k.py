import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CitationMapsK(unittest.TestCase):
 def test_four_maps_are_source_only_and_have_manifest_cells(self):
  for c in ["switch-pro","dualsense","dualshock4","xbox360"]:
   s=(ROOT/"docs"/(c+"-citation-map.md")).read_text()
   self.assertIn("uncited",s)
   self.assertIn("acceptance/",s)
   self.assertIn("not run",s.lower())
   self.assertIn("Research parity, part 2: consumers and decisions",s)
   self.assertIn("linux.uinput",s)
   self.assertIn("linux.uhid.usb",s)
   self.assertIn("not-supported",s)
  a=(ROOT/"docs/dualshock4-citation-map.md").read_text()
  self.assertIn("DS4-USB",a)
  self.assertIn("DS4-BT",a)
  d=(ROOT/"docs/dualsense-citation-map.md").read_text()
  for x in ("0x03","0x05","0x09","0x20","No output reports"):
   self.assertIn(x.lower(),d.lower())
if __name__=="__main__": unittest.main()
