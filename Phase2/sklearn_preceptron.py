import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import Perceptron
from sklearn.metrics import classification_report

url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/tic-tac-toe/tic-tac-toe.data'
df = pd.read_csv(url, header=None)
mapping = {'x': 1, 'o': -1, 'b': 0}
for col in df.columns[:-1]:
    df[col] = df[col].map(mapping)
X = df.iloc[:, :-1]
y = df.iloc[:, -1]
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
perceptron = Perceptron()
perceptron.fit(X_train, y_train)
predictions = perceptron.predict(X_test)
print("Predictions:", predictions)
report = classification_report(y_test, predictions)
print("Classification Report:\n", report)