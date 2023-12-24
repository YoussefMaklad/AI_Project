from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from ucimlrepo import fetch_ucirepo

# Fetch The Dataset
iris = fetch_ucirepo(id=53)

# Data (as pandas dataframes)
X = iris.data.features
y = iris.data.targets

# Convert Data to Test, Train (Common Practise)
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=13)

y_train = y_train.values.ravel()
y_test = y_test.values.ravel()

# Train The Classifier
logistic_classifier = LogisticRegression(random_state=13)
logistic_classifier.fit(x_train, y_train)
y_pred = logistic_classifier.predict(x_test)

# Evaluate the classifier
accuracy = accuracy_score(y_pred, y_test)
report = classification_report(y_pred, y_test)

# Display the Evaluation Results
print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:\n", report)
