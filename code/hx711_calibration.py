"""
HX711 Load Cell Calibration Script

This script was used to calibrate the load cell for the Smart Donation Sorting System.
It calculates:
- TARE value
- Calibration ratio

These values can then be copied into the main SDSS control program.
"""

import time
from hx711 import HX711


DAT_PIN = 6
CLK_PIN = 13

hx = HX711(dout_pin=DAT_PIN, pd_sck_pin=CLK_PIN)


def get_average_raw(samples=20):
    """
    Reads multiple raw values from the HX711 and returns the average.
    """
    values = []

    for _ in range(samples):
        value = hx.get_raw_data_mean()

        if value is not None:
            values.append(value)

        time.sleep(0.1)

    if len(values) == 0:
        return None

    return sum(values) / len(values)


try:
    print("Make sure the tray is empty.")
    input("Press Enter when ready...")

    print("Reading tare value...")
    tare_value = get_average_raw(samples=20)

    if tare_value is None:
        print("Error: No HX711 reading detected.")
        exit()

    print("Tare raw value:", tare_value)

    known_weight = float(input("Enter known weight in grams: "))

    print("Place the known weight on the tray.")
    input("Press Enter when the weight is stable...")

    print("Reading loaded value...")
    loaded_value = get_average_raw(samples=20)

    if loaded_value is None:
        print("Error: No HX711 reading detected.")
        exit()

    print("Loaded raw value:", loaded_value)

    calibration_ratio = (loaded_value - tare_value) / known_weight

    print()
    print("Calibration complete.")
    print("TARE =", tare_value)
    print("CAL_RATIO =", calibration_ratio)

except KeyboardInterrupt:
    print("\nCalibration stopped.")
