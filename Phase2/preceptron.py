import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report


class Perceptron:
    def __init__(self, input_size):
        self.weights = np.random.rand(input_size)

    def activation_function(self, result):
        if result > 0:
            return 1
        return 0

    def update_weight(self, Y, T, inputs, learning_rate):
        error = T - Y
        inputs_np = np.array(inputs)
        self.weights += learning_rate * error * inputs_np

    def predict(self, inputs):
        result = np.dot(inputs, self.weights)
        return self.activation_function(result)

    def test(self, test):
        predict = []
        for t in test:
            predict.append(self.predict(t))
        return predict

    def train(self, inputs, targets, learning_rate=0.1, epochs=1000):
        for epoch in range(epochs):
            zero_error = True
            for input_data, target in zip(inputs, targets):
                predict = self.predict(input_data)
                if target - predict != 0:
                    zero_error = False
                self.update_weight(predict, target, input_data, learning_rate)
            if zero_error:
                break


np.random.seed(42)
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/tic-tac-toe/tic-tac-toe.data"
df = pd.read_csv(url, header=None)
mapping = {"x": 1, "o": -1, "b": 0}
for col in df.columns[:-1]:
    df[col] = df[col].map(mapping)
X = df.iloc[:, :-1].values.tolist()
y = df.iloc[:, -1]
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
input_size = len(X_train[0])
perceptron = Perceptron(input_size)
perceptron.train(X_train, y_train)
predictions = perceptron.test(X_test)
print("Predictions:", predictions)
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)
report = classification_report(y_test, predictions)
print("Classification Report:\n", report)
