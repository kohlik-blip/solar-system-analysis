"""
Raw planetary data for the Solar System backend.

Values are stored in *absolute* units (kilograms, kilometres, etc.) rather
than "relative to Earth", because the analysis layer needs real physical
quantities to compute things like density and surface gravity. Anything that
is "relative to Earth" or a fun fact belongs in the presentation layer, not
here.

Sources: NASA planetary fact sheets (approximate mean values). Moon counts
and gas-giant cloud-top temperatures vary by source and over time.
"""

# name -> raw measurements
PLANETS = {
    "Mercury": {
        "order": 1,
        "mass_kg": 3.301e23,
        "radius_km": 2439.7,
        "distance_au": 0.387,
        "avg_temp_c": 167,
        "orbital_period_days": 88.0,
        "moons": 0,
    },
    "Venus": {
        "order": 2,
        "mass_kg": 4.867e24,
        "radius_km": 6051.8,
        "distance_au": 0.723,
        "avg_temp_c": 464,
        "orbital_period_days": 224.7,
        "moons": 0,
    },
    "Earth": {
        "order": 3,
        "mass_kg": 5.972e24,
        "radius_km": 6371.0,
        "distance_au": 1.000,
        "avg_temp_c": 15,
        "orbital_period_days": 365.25,
        "moons": 1,
    },
    "Mars": {
        "order": 4,
        "mass_kg": 6.417e23,
        "radius_km": 3389.5,
        "distance_au": 1.524,
        "avg_temp_c": -63,
        "orbital_period_days": 687.0,
        "moons": 2,
    },
    "Jupiter": {
        "order": 5,
        "mass_kg": 1.898e27,
        "radius_km": 69911.0,
        "distance_au": 5.203,
        "avg_temp_c": -108,
        "orbital_period_days": 4332.6,
        "moons": 95,
    },
    "Saturn": {
        "order": 6,
        "mass_kg": 5.683e26,
        "radius_km": 58232.0,
        "distance_au": 9.537,
        "avg_temp_c": -139,
        "orbital_period_days": 10759.2,
        "moons": 146,
    },
    "Uranus": {
        "order": 7,
        "mass_kg": 8.681e25,
        "radius_km": 25362.0,
        "distance_au": 19.191,
        "avg_temp_c": -195,
        "orbital_period_days": 30688.5,
        "moons": 28,
    },
    "Neptune": {
        "order": 8,
        "mass_kg": 1.024e26,
        "radius_km": 24622.0,
        "distance_au": 30.069,
        "avg_temp_c": -201,
        "orbital_period_days": 60195.0,
        "moons": 16,
    },
}
