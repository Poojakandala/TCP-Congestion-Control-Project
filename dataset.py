# import pandas as pd
# import numpy as np
   
# # Number of samples
# n = 5000
# np.random.seed(42)

# # Generate synthetic TCP metrics
# rtt = np.random.uniform(10, 300, n)             # Round Trip Time (ms)
# throughput = np.random.uniform(50, 1000, n)     # Throughput (KB/s)
# packet_loss = np.random.uniform(0, 10, n)       # Packet loss rate (%)
# window_size = np.random.uniform(1, 64, n)       # TCP window size (KB)

# # Label: 1 = congested, 0 = not congested
# congested = np.where((rtt > 200) | (packet_loss > 5) | (throughput < 200), 1, 0)

# # Create DataFrame
# data = pd.DataFrame({
#     'rtt': rtt,
#     'throughput': throughput,
#     'packet_loss': packet_loss,
#     'window_size': window_size,
#     'congested': congested
# })

# # Save to CSV in expo folder
# data.to_csv('D:/expo/tcp_metrics.csv', index=False)
# print("✅ Dataset created successfully at D:/expo/tcp_metrics.csv")


# import pandas as pd
# import numpy as np

# num_samples = 1000

# data = {
#     'window_size': np.random.randint(10, 1000, size=num_samples),
#     'rtt': np.random.uniform(10, 100, size=num_samples),
#     'throughput': np.random.uniform(1, 100, size=num_samples),
#     'bytes_in_flight': np.random.randint(100, 10000, size=num_samples),
#     'packet_loss': np.random.uniform(0, 0.05, size=num_samples),
#     'congested': np.random.choice([0, 1], size=num_samples)
# }

# df = pd.DataFrame(data)
# df.to_csv('tcp_network_data.csv', index=False)
# print("Data saved as tcp_network_data.csv")


import numpy as np
import pandas as pd

n_samples = 1000
np.random.seed(42)

# Congestion flag (simulate ~30% congestion)
congested = np.random.binomial(1, 0.3, n_samples)

# RTT: lower in non-congested, higher in congested
rtt = np.where(
    congested == 1,
    np.random.normal(120, 30, n_samples),  # Congested: avg 120ms ±30ms
    np.random.normal(40, 10, n_samples)   # Non-congested: avg 40ms ±10ms
)

# Throughput: lower if congested, higher if not
throughput = np.where(
    congested == 1,
    np.random.normal(12, 2, n_samples),   # Congested: avg 12Mbps ±2Mbps
    np.random.normal(45, 8, n_samples)    # Non-congested: avg 45Mbps ±8Mbps
)

# Window size: smaller if congested
window_size = np.where(
    congested == 1,
    np.random.normal(450, 60, n_samples), # Congested: avg 450 ±60
    np.random.normal(1200, 200, n_samples)# Non-congested: avg 1200 ±200
)

# Bytes in flight: usually higher with higher window/throughput
bytes_in_flight = window_size * np.random.uniform(5, 10, n_samples)

# Packet loss: low if not congested, moderate-high if congested
packet_loss = np.where(
    congested == 1,
    np.clip(np.random.normal(0.035, 0.01, n_samples), 0.01, 0.08), # Congested: ~1%-8%
    np.clip(np.random.normal(0.008, 0.003, n_samples), 0, 0.02)    # Non-congested: up to 2%
)

# Time taken to resend after congestion (realistic values)
resend_time_after_congestion = np.where(
    congested == 1,
    np.random.normal(200, 50, n_samples),  # Congested: avg 200ms ±50ms
    0                                     # Non-congested: no resend
)

# Clip values to keep everything plausible
window_size = np.clip(window_size, 200, 2000)
rtt = np.clip(rtt, 10, 300)
throughput = np.clip(throughput, 1, 100)
bytes_in_flight = np.clip(bytes_in_flight, 1000, 15000)
resend_time_after_congestion = np.clip(resend_time_after_congestion, 0, 400)

# Assemble DataFrame
df = pd.DataFrame({
    'window_size': window_size.astype(int),
    'rtt': rtt,
    'throughput': throughput,
    'bytes_in_flight': bytes_in_flight.astype(int),
    'packet_loss': packet_loss,
    'congested': congested,
    'resend_time_after_congestion': resend_time_after_congestion
})

# Save for R analysis
df.to_csv('tcp_network_data.csv', index=False)
print(df.head())
