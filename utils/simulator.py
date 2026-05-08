import random
from datetime import datetime

def generate_data():
    now = datetime.now()

    hour = now.hour

    # Realistic electricity usage patterns
    if 6 <= hour < 9:
        base_usage = random.uniform(2.5, 4.5)

    elif 9 <= hour < 17:
        base_usage = random.uniform(1.5, 3.0)

    elif 17 <= hour < 23:
        base_usage = random.uniform(3.5, 6.5)

    else:
        base_usage = random.uniform(0.8, 2.0)

    # Random spike simulation
    spike = random.choice([0, 0, 0, 1.5])

    usage = round(base_usage + spike, 2)

    voltage = round(random.uniform(220, 240), 2)

    current = round((usage * 1000) / voltage, 2)

    return {
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "usage_kwh": usage,
        "voltage": voltage,
        "current": current
    }