from typing import List, Dict
import math
import random

class DemandPredictor:
    def __init__(self):
        self.weights = []
        self.bias = 0
        self.is_trained = False

    def train(self, historical_data: Dict[str, List[float]], features: List[List[float]]):
        """
        Train a simple linear regression model
        """
        X = features
        y = [data[-1] for data in historical_data.values()]
        
        # Initialize weights randomly
        num_features = len(X[0])
        self.weights = [random.uniform(-1, 1) for _ in range(num_features)]
        self.bias = random.uniform(-1, 1)
        
        # Simple gradient descent
        learning_rate = 0.01
        epochs = 100
        
        for _ in range(epochs):
            for i in range(len(X)):
                prediction = self._predict_raw(X[i])
                error = prediction - y[i]
                
                # Update weights and bias
                for j in range(len(self.weights)):
                    self.weights[j] -= learning_rate * error * X[i][j]
                self.bias -= learning_rate * error
        
        self.is_trained = True

    def _predict_raw(self, features: List[float]) -> float:
        """
        Make a raw prediction using linear regression
        """
        result = self.bias
        for w, x in zip(self.weights, features):
            result += w * x
        return result

    def predict(self, area_id: str, features: List[float]) -> float:
        """
        Predict food demand for a specific area
        """
        if not self.is_trained:
            raise ValueError("Model is not trained yet")
        
        prediction = self._predict_raw(features)
        return max(0, prediction) * 1.1  # Add 10% buffer and ensure non-negative