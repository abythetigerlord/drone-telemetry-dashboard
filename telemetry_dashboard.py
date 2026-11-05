"""Create a summary report from a drone telemetry CSV file."""

import csv
from pathlib import Path


def load_telemetry(filename):
    with Path(filename).open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def summarize(rows):
    if not rows:
        raise ValueError("Telemetry file contains no readings.")
    fields = ["altitude_m", "speed_mps", "battery_percent", "temperature_c"]
    values = {field: [float(row[field]) for row in rows] for field in fields}
    return {
        "readings": len(rows),
        "max_altitude_m": max(values["altitude_m"]),
        "max_speed_mps": max(values["speed_mps"]),
        "starting_battery": values["battery_percent"][0],
        "ending_battery": values["battery_percent"][-1],
        "average_temperature_c": sum(values["temperature_c"]) / len(rows),
    }


def main():
    report = summarize(load_telemetry(Path(__file__).with_name("telemetry.csv")))
    print("Drone Telemetry Dashboard")
    print(f"Readings: {report['readings']}")
    print(f"Maximum altitude: {report['max_altitude_m']:.1f} m")
    print(f"Maximum speed: {report['max_speed_mps']:.1f} m/s")
    print(f"Battery change: {report['starting_battery']:.0f}% -> {report['ending_battery']:.0f}%")
    print(f"Average temperature: {report['average_temperature_c']:.1f} °C")


if __name__ == "__main__":
    main()

