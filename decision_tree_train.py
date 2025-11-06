# decision_tree_train.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Step 1: Load dataset
data = pd.read_csv("tcp_congestion_results_r.csv")

print("Dataset Loaded Successfully ✅")
print("Columns:", data.columns)
print(data.head())

# Step 2: Separate features (X) and target (y)
# ⚠️ Replace 'target_column_name' with your actual label column (example: 'congestion')
X = data.drop('Actual', axis=1)
y = data['Actual']


# Step 3: Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train Decision Tree Classifier
model = DecisionTreeClassifier(criterion='entropy', max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Step 5: Make predictions
y_pred = model.predict(X_test)

# Step 6: Evaluate the model
print("\n✅ Model Evaluation:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Step 7: Save the trained model
joblib.dump(model, "decision_tree_model.pkl")
print("\nModel saved as 'decision_tree_model.pkl' ✅")
