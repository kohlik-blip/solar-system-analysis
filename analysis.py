"""
Analysis layer for the Solar System backend.

This module does the actual "interpreting" of the data. It has no web code in
it at all -- every function takes plain data and returns plain data, so you can
import it into the Flask app OR just run this file directly to print a report:

    python3 analysis.py

Keeping the analysis separate from the server is the important design idea: the
logic is testable on its own, and the API in app.py is just a thin wrapper
around these functions.
"""

import math
from planets_data import PLANETS

# Physical constants
G = 6.674e-11          # gravitational constant, m^3 kg^-1 s^-2
EARTH_MASS_KG = 5.972e24
EARTH_GRAVITY = 9.81   # m/s^2, for "relative to Earth" comparisons


# ---------------------------------------------------------------------------
# Deriving physical properties from the raw numbers
# ---------------------------------------------------------------------------
def derived_properties(name):
    """Compute physical properties for one planet from its mass and radius."""
    p = PLANETS[name]
    mass = p["mass_kg"]
    radius_m = p["radius_km"] * 1000.0

    volume_m3 = (4.0 / 3.0) * math.pi * radius_m ** 3
    density = mass / volume_m3                          # kg/m^3
    gravity = G * mass / radius_m ** 2                  # m/s^2
    escape_velocity = math.sqrt(2 * G * mass / radius_m)  # m/s

    return {
        "name": name,
        "order": p["order"],
        "mass_kg": mass,
        "mass_vs_earth": round(mass / EARTH_MASS_KG, 3),
        "radius_km": p["radius_km"],
        "diameter_km": round(p["radius_km"] * 2),
        "distance_au": p["distance_au"],
        "avg_temp_c": p["avg_temp_c"],
        "avg_temp_f": round(p["avg_temp_c"] * 9 / 5 + 32),
        "orbital_period_days": p["orbital_period_days"],
        "orbital_period_years": round(p["orbital_period_days"] / 365.25, 2),
        "moons": p["moons"],
        # --- derived ---
        "density_kg_m3": round(density),
        "surface_gravity_m_s2": round(gravity, 2),
        "gravity_vs_earth": round(gravity / EARTH_GRAVITY, 2),
        "escape_velocity_km_s": round(escape_velocity / 1000.0, 2),
        "classification": classify(name),
    }


def all_planets():
    """Derived properties for every planet, in orbital order."""
    return [derived_properties(n) for n in
            sorted(PLANETS, key=lambda n: PLANETS[n]["order"])]


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------
def classify(name):
    """
    Group a planet by radius. The thresholds are chosen so the result matches
    the conventional composition-based grouping (terrestrial / gas giant / ice
    giant), but here it's *derived* from the size rather than hard-coded.
    """
    r = PLANETS[name]["radius_km"]
    if r < 15000:
        return "Terrestrial"
    if r > 50000:
        return "Gas giant"
    return "Ice giant"


# ---------------------------------------------------------------------------
# Summary statistics
# ---------------------------------------------------------------------------
def _stat_block(planets, key, label, unit=""):
    values = [(p["name"], p[key]) for p in planets]
    nums = [v for _, v in values]
    hi = max(values, key=lambda x: x[1])
    lo = min(values, key=lambda x: x[1])
    return {
        "metric": label,
        "unit": unit,
        "min": {"planet": lo[0], "value": lo[1]},
        "max": {"planet": hi[0], "value": hi[1]},
        "mean": round(sum(nums) / len(nums), 2),
    }


def summary():
    """Min / max / mean for the headline metrics, with which planet holds each."""
    planets = all_planets()
    return {
        "planet_count": len(planets),
        "metrics": [
            _stat_block(planets, "diameter_km", "Diameter", "km"),
            _stat_block(planets, "avg_temp_c", "Average temperature", "C"),
            _stat_block(planets, "distance_au", "Distance from Sun", "AU"),
            _stat_block(planets, "density_kg_m3", "Density", "kg/m3"),
            _stat_block(planets, "surface_gravity_m_s2", "Surface gravity", "m/s2"),
            _stat_block(planets, "moons", "Moons", "count"),
        ],
    }


# ---------------------------------------------------------------------------
# Rankings
# ---------------------------------------------------------------------------
def rankings():
    """Ordered lists for a few interesting metrics (descending)."""
    planets = all_planets()

    def top(key):
        return [{"planet": p["name"], "value": p[key]}
                for p in sorted(planets, key=lambda p: p[key], reverse=True)]

    return {
        "largest": top("diameter_km"),
        "hottest": top("avg_temp_c"),
        "densest": top("density_kg_m3"),
        "strongest_gravity": top("surface_gravity_m_s2"),
        "most_moons": top("moons"),
    }


# ---------------------------------------------------------------------------
# Comparison between two planets
# ---------------------------------------------------------------------------
def compare(name_a, name_b):
    """Side-by-side comparison with ratios of a few key numbers."""
    a = derived_properties(name_a)
    b = derived_properties(name_b)
    keys = [
        ("diameter_km", "Diameter (km)"),
        ("mass_vs_earth", "Mass (x Earth)"),
        ("surface_gravity_m_s2", "Surface gravity (m/s2)"),
        ("avg_temp_c", "Avg temperature (C)"),
        ("distance_au", "Distance from Sun (AU)"),
        ("moons", "Moons"),
    ]
    rows = []
    for key, label in keys:
        va, vb = a[key], b[key]
        ratio = round(va / vb, 2) if vb not in (0, 0.0) else None
        rows.append({"metric": label, name_a: va, name_b: vb,
                     "ratio_a_over_b": ratio})
    return {"a": name_a, "b": name_b, "rows": rows}


# ---------------------------------------------------------------------------
# Correlation: does distance from the Sun predict temperature?
# ---------------------------------------------------------------------------
def _pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return cov / (sx * sy) if sx and sy else 0.0


def distance_temp_correlation():
    """
    Pearson correlation between distance from the Sun and average temperature,
    plus any planet that breaks the 'farther = colder' trend. (Venus does: it's
    hotter than Mercury despite being farther out, because of its thick CO2
    atmosphere -- a nice example of data that needs interpreting, not just
    sorting.)
    """
    planets = all_planets()
    dist = [p["distance_au"] for p in planets]
    temp = [p["avg_temp_c"] for p in planets]
    r = _pearson(dist, temp)

    # Flag planets that are hotter than a closer-in neighbour.
    by_distance = sorted(planets, key=lambda p: p["distance_au"])
    outliers = []
    for inner, outer in zip(by_distance, by_distance[1:]):
        if outer["avg_temp_c"] > inner["avg_temp_c"]:
            outliers.append({
                "planet": outer["name"],
                "note": (outer["name"] + " is warmer than " + inner["name"]
                         + " despite being farther from the Sun"),
            })

    strength = "strong" if abs(r) > 0.7 else "moderate" if abs(r) > 0.4 else "weak"
    direction = "negative (farther = colder)" if r < 0 else "positive"
    return {
        "pearson_r": round(r, 3),
        "interpretation": strength + " " + direction + " relationship",
        "trend_breakers": outliers,
    }


# ---------------------------------------------------------------------------
# Standalone report
# ---------------------------------------------------------------------------
def print_report():
    line = "=" * 60
    print(line)
    print("SOLAR SYSTEM DATA ANALYSIS")
    print(line)

    print("\nDERIVED PROPERTIES")
    hdr = "{:<9}{:>8}{:>11}{:>9}{:>8}  {}"
    print(hdr.format("Planet", "Dens.", "Gravity", "Escape", "Moons", "Type"))
    print(hdr.format("", "kg/m3", "m/s2", "km/s", "", ""))
    for p in all_planets():
        print(hdr.format(
            p["name"], p["density_kg_m3"], p["surface_gravity_m_s2"],
            p["escape_velocity_km_s"], p["moons"], p["classification"]))

    print("\nSUMMARY (extremes)")
    for m in summary()["metrics"]:
        print("  {:<22} lowest: {:<9} highest: {:<9} mean: {}".format(
            m["metric"], m["min"]["planet"], m["max"]["planet"], m["mean"]))

    print("\nDISTANCE vs TEMPERATURE")
    c = distance_temp_correlation()
    print("  Pearson r = {}  ->  {}".format(c["pearson_r"], c["interpretation"]))
    for o in c["trend_breakers"]:
        print("  ! " + o["note"])

    print("\nEXAMPLE COMPARISON: Earth vs Mars")
    for row in compare("Earth", "Mars")["rows"]:
        print("  {:<24} Earth={:<8} Mars={:<8} (ratio {})".format(
            row["metric"], row["Earth"], row["Mars"], row["ratio_a_over_b"]))
    print(line)


if __name__ == "__main__":
    print_report()
