import numpy as np
import json
import pickle
import random
from typing import List, Tuple, Dict

class FinanceChatbot:
    def __init__(self):
        self.words = []
        self.tags = []
        self.documents = []
        self.ignore_chars = ['?', '!', '.', ',']
        self.weights_input_hidden = None
        self.weights_hidden_output = None
        self.bias_hidden = None
        self.bias_output = None

    def tokenize(self, sentence: str) -> List[str]:
        return sentence.lower().split()

    def stem(self, word: str) -> str:
        return word.lower()

    def bag_of_words(self, sentence: str) -> np.ndarray:
        sentence_words = self.tokenize(sentence)
        sentence_words = [self.stem(word) for word in sentence_words]

        bag = np.zeros(len(self.words), dtype=np.float32)
        for idx, word in enumerate(self.words):
            if word in sentence_words:
                bag[idx] = 1.0

        return bag

    def sigmoid(self, x: np.ndarray) -> np.ndarray:
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def sigmoid_derivative(self, x: np.ndarray) -> np.ndarray:
        return x * (1 - x)

    def softmax(self, x: np.ndarray) -> np.ndarray:
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum()

    def forward_pass(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        hidden = self.sigmoid(np.dot(X, self.weights_input_hidden) + self.bias_hidden)
        output = self.softmax(np.dot(hidden, self.weights_hidden_output) + self.bias_output)
        return hidden, output

    def prepare_training_data(self, training_file: str) -> Tuple[np.ndarray, np.ndarray]:
        with open(training_file, 'r') as f:
            intents = json.load(f)

        for intent in intents:
            tag = intent['tag']
            if tag not in self.tags:
                self.tags.append(tag)

            for pattern in intent['patterns']:
                words = self.tokenize(pattern)
                self.words.extend(words)
                self.documents.append((words, tag))

        self.words = sorted(set([self.stem(w) for w in self.words if w not in self.ignore_chars]))
        self.tags = sorted(set(self.tags))

        training_data = []
        output_data = []

        for doc in self.documents:
            bag = []
            word_patterns = [self.stem(w) for w in doc[0]]

            for word in self.words:
                bag.append(1.0 if word in word_patterns else 0.0)

            output_row = [0] * len(self.tags)
            output_row[self.tags.index(doc[1])] = 1

            training_data.append(bag)
            output_data.append(output_row)

        return np.array(training_data, dtype=np.float32), np.array(output_data, dtype=np.float32)

    def train(self, training_file: str, hidden_neurons: int = 16, learning_rate: float = 0.01, epochs: int = 2000):
        X_train, y_train = self.prepare_training_data(training_file)

        input_neurons = len(self.words)
        output_neurons = len(self.tags)

        np.random.seed(42)
        self.weights_input_hidden = np.random.randn(input_neurons, hidden_neurons) * 0.5
        self.weights_hidden_output = np.random.randn(hidden_neurons, output_neurons) * 0.5
        self.bias_hidden = np.zeros((1, hidden_neurons))
        self.bias_output = np.zeros((1, output_neurons))

        print(f"Training on {len(X_train)} samples...")
        print(f"Vocabulary size: {input_neurons}")
        print(f"Number of intents: {output_neurons}")

        for epoch in range(epochs):
            for i in range(len(X_train)):
                X = X_train[i:i+1]
                y = y_train[i:i+1]

                hidden, output = self.forward_pass(X)

                output_error = y - output
                output_delta = output_error

                hidden_error = output_delta.dot(self.weights_hidden_output.T)
                hidden_delta = hidden_error * self.sigmoid_derivative(hidden)

                self.weights_hidden_output += hidden.T.dot(output_delta) * learning_rate
                self.bias_output += np.sum(output_delta, axis=0, keepdims=True) * learning_rate
                self.weights_input_hidden += X.T.dot(hidden_delta) * learning_rate
                self.bias_hidden += np.sum(hidden_delta, axis=0, keepdims=True) * learning_rate

            if (epoch + 1) % 200 == 0:
                loss = np.mean(np.square(y_train - self.forward_pass(X_train)[1]))
                print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss:.4f}")

        print("Training complete!")

    def predict(self, sentence: str, threshold: float = 0.25) -> Dict:
        bow = self.bag_of_words(sentence).reshape(1, -1)
        _, output = self.forward_pass(bow)

        predicted_idx = np.argmax(output)
        predicted_prob = output[0][predicted_idx]

        if predicted_prob > threshold:
            predicted_tag = self.tags[predicted_idx]
            return {
                'tag': predicted_tag,
                'probability': float(predicted_prob)
            }
        else:
            return {
                'tag': 'unknown',
                'probability': float(predicted_prob)
            }

    def get_response(self, sentence: str, intents_file: str) -> str:
        prediction = self.predict(sentence)
        tag = prediction['tag']

        if tag == 'unknown':
            return "I'm not sure about that. Could you rephrase your question or ask about investing, budgeting, retirement, or other finance topics?"

        with open(intents_file, 'r') as f:
            intents = json.load(f)

        for intent in intents:
            if intent['tag'] == tag:
                return random.choice(intent['responses'])

        return "I'm here to help with finance questions!"

    def save_model(self, filepath: str):
        model_data = {
            'words': self.words,
            'tags': self.tags,
            'weights_input_hidden': self.weights_input_hidden,
            'weights_hidden_output': self.weights_hidden_output,
            'bias_hidden': self.bias_hidden,
            'bias_output': self.bias_output
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath: str):
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.words = model_data['words']
        self.tags = model_data['tags']
        self.weights_input_hidden = model_data['weights_input_hidden']
        self.weights_hidden_output = model_data['weights_hidden_output']
        self.bias_hidden = model_data['bias_hidden']
        self.bias_output = model_data['bias_output']
        print(f"Model loaded from {filepath}")


if __name__ == "__main__":
    chatbot = FinanceChatbot()

    training_file = "training_data.json"
    model_file = "finance_model.pkl"

    print("Training the finance chatbot...")
    chatbot.train(training_file, hidden_neurons=16, learning_rate=0.01, epochs=2000)

    chatbot.save_model(model_file)

    print("\n" + "="*50)
    print("Testing the chatbot:")
    print("="*50)

    test_questions = [
        "Hello",
        "What are stocks?",
        "How do I start investing?",
        "Tell me about retirement planning",
        "What is an emergency fund?",
        "How to pay off debt?"
    ]

    for question in test_questions:
        response = chatbot.get_response(question, training_file)
        print(f"\nQ: {question}")
        print(f"A: {response}")
