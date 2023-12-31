import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/tic-tac-toe/tic-tac-toe.data"
df = pd.read_csv(url, header=None)
mapping = {"x": 1, "o": -1, "b": 0}
for col in df.columns[:-1]:
    df[col] = df[col].map(mapping)
X = df.iloc[:, :-1]
y = df.iloc[:, -1]
x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=13
)
logistic_classifier = LogisticRegression(random_state=13)
logistic_classifier.fit(x_train, y_train)
y_pred = logistic_classifier.predict(x_test)
accuracy = accuracy_score(y_pred, y_test)
report = classification_report(y_pred, y_test)
print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:\n", report)
