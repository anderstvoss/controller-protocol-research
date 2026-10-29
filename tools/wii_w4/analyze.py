"""Derive bounded W4 outcomes from sanitized own-device SDL summaries."""


def assess(case, observation, outputs):
    held = (observation.get('hidapi_open') is True and
            observation.get('raw_open') is True and
            observation.get('window_ms', 0) >= 60_000 and
            observation.get('polls', 0) > 0 and
            observation.get('disconnected_polls', 1) == 0 and
            observation.get('removed_events', 1) == 0)
    buttons = any(mask == 3 for mask in observation.get('button_seen_masks', []))
    axes = any(axis['max'] > axis['min'] for axis in observation.get('axes', []))
    sensors = observation.get('sensors', {})

    def varied(name):
        sample = sensors.get(name, {})
        return (sample.get('capable') is True and sample.get('enabled') is True and
                sample.get('samples', 0) > 0 and any(
                    high > low for low, high in zip(sample.get('min', []), sample.get('max', []))))

    led_states = {tuple(row['value']['leds']) for row in outputs}
    # Retained LED intent can succeed even when SDL omits its advisory capability flag.
    led = (observation.get('player_index_1_request') is True and
           observation.get('player_index_2_request') is True and
           (False, True, False, False) in led_states and
           (False, False, True, False) in led_states)
    need_axes = case in ('nunchuk', 'classic', 'motionplus-nunchuk')
    need_accel = case != 'classic'
    need_gyro = case.startswith('motionplus')
    complete = held and buttons and (axes or not need_axes) and led and (
        varied('accelerometer') or not need_accel) and (varied('gyro') or not need_gyro)
    return {'claim_held': held, 'button_variation': buttons, 'axis_variation': axes,
            'axis_required': need_axes, 'accelerometer_variation': varied('accelerometer'),
            'accelerometer_required': need_accel, 'gyro_variation': varied('gyro'),
            'gyro_required': need_gyro, 'player_led_intent': led,
            'disposition': 'passed' if complete else 'blocked'}
