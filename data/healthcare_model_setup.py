import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load real healthcare dataset
df = pd.read_csv("data/heart_disease_uci.csv")

print("Dataset shape:", df.shape)
print("Columns:", df.columns)

# Drop rows with missing values
df = df.dropna()

# Convert target to binary
# num = 0 -> No disease
# num > 0 -> Disease present
df["num"] = df["num"].apply(lambda x: 1 if x > 0 else 0)

# Features and target
X = df.drop("num", axis=1)
y = df["num"]

# Convert categorical columns to numeric
X = pd.get_dummies(X, drop_first=True)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Logistic Regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Healthcare model trained successfully")
print("Accuracy:", accuracy)
