import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict, train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset
df = pd.read_csv("tcp_network_data.csv")

# Encode target as numeric for RMSE and R^2 calculation
df['congested_num'] = df['congested'].astype('category').cat.codes

# Features and target
X = df[['window_size', 'rtt', 'throughput', 'bytes_in_flight', 'packet_loss', 'resend_time_after_congestion']]
y = df['congested_num']

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize Random Forest classifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)

# Cross-validated predictions on training set
y_train_pred = cross_val_predict(rf, X_train, y_train, cv=10)

# Train on full training set
rf.fit(X_train, y_train)

# Predict on test set
y_test_pred = rf.predict(X_test)

# Calculate RMSE on test set
rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

# Calculate R^2 on test set
r2 = r2_score(y_test, y_test_pred)

print(f"RMSE on test data: {rmse:.4f}")
print(f"R-squared on test data: {r2:.4f}")
