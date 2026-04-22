import pandas as pd
import numpy as np

from sklearn.datasets import fetch_openml # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.metrics import accuracy_score # type: ignore

# Load dataset
adult = fetch_openml("adult", version=2, as_frame=True)
df = adult.frame

print("Dataset loaded:", df.shape)

# Clean data
df = df.replace("?", np.nan)
df = df.dropna()

# Encode target
# Encode target variable (CORRECT column name)
df['class'] = df['class'].apply(lambda x: 1 if x == '>50K' else 0)

X = df.drop(columns=['class'])
y = df['class']



# Convert categorical → numeric
X = pd.get_dummies(X, drop_first=True)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save audit data
audit_df = X_test.copy()
audit_df['actual'] = y_test.values
audit_df['predicted'] = y_pred
audit_df.to_csv("data/adult_audit_data.csv", index=False)

print("Audit data saved")
