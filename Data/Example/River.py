import cdsapi

c = cdsapi.Client()

c.retrieve(
    'satellite-precipitation-microwave-infrared',
    {
        'format': 'netcdf',
        'variable': ['all'],
        'year': [str(y) for y in range(2002, 2024)],
        'month': [f'{m:02d}' for m in range(1, 13)],
        'day':["01"],
        "time_aggregation": "monthly",
        'area': [36.3901, 37.9681, 34.4157, 41.0552],  # [North, West, South, East] — Euphrates region
    },
    'euphrates_precipitation.zip'  # New file name
)
