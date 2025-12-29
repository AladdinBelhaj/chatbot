from flask import Flask, request, jsonify
from flask_cors import CORS
from model import FinanceChatbot
import os

app = Flask(__name__)
CORS(app)

chatbot = FinanceChatbot()
model_file = "finance_model.pkl"
training_file = "training_data.json"

if os.path.exists(model_file):
    print("Loading existing model...")
    chatbot.load_model(model_file)
else:
    print("Training new model...")
    chatbot.train(training_file)
    chatbot.save_model(model_file)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        response = chatbot.get_response(message, training_file)
        prediction = chatbot.predict(message)

        return jsonify({
            'response': response,
            'confidence': prediction['probability'],
            'intent': prediction['tag']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': chatbot.weights_input_hidden is not None})

@app.route('/api/retrain', methods=['POST'])
def retrain():
    try:
        print("Retraining model...")
        chatbot.train(training_file)
        chatbot.save_model(model_file)
        return jsonify({'message': 'Model retrained successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
