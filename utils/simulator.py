import numpy as np
from datetime import datetime


def generate_live_data():

    data = {
        "timestamp": datetime.now(),
        "usage_kwh": round(np.random.uniform(1.5, 8.5), 2),
        "voltage": round(np.random.uniform(220, 240), 2),
        "current": round(np.random.uniform(5, 15), 2)
    }

    return data