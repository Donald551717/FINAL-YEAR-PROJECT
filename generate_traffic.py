import pandas as pd
import numpy as np
import random

def generate_data(n=100):
    data = {
        'Flow Duration': np.random.randint(1000, 100000, size=n),
        'Total Fwd Packets': np.random.randint(5, 100, size=n),
        'Total Backward Packets': np.random.randint(5, 100, size=n),
        'Flow Bytes/s': np.random.randint(300, 1500, size=n),
        'Flow Packets/s': np.random.rand(n) * 10,
        'Label': [random.choice(['BENIGN', 'MALICIOUS']) for _ in range(n)]
    }
    df = pd.DataFrame(data)
    df.to_csv("sample_network_traffic.csv", index=False)
    print("✅ sample_network_traffic.csv generated!")

if __name__ == "__main__":
    generate_data(200)
    