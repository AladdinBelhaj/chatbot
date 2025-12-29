# Finance AI Chatbot

A trained finance chatbot powered by a custom neural network built from scratch in Python. The chatbot can answer questions about investing, budgeting, retirement planning, debt management, and more.

## Features

- **Custom Neural Network**: Built from scratch using NumPy with bag-of-words representation
- **Finance Knowledge**: Trained on 20+ finance topics with 100+ Q&A patterns
- **Real-time Chat Interface**: Modern React UI with Tailwind CSS
- **Conversation History**: Stores all conversations in Supabase database
- **Confidence Scores**: Shows model confidence for each response
- **Session Tracking**: Groups conversations by session for analysis

## Tech Stack

### Backend
- Python 3.8+
- NumPy (neural network)
- Flask (API server)
- Flask-CORS

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Lucide React (icons)
- Supabase (database)

## Project Structure

```
├── backend/
│   ├── app.py              # Flask API server
│   ├── model.py            # Neural network implementation
│   ├── training_data.json  # Finance Q&A training data
│   ├── requirements.txt    # Python dependencies
│   └── finance_model.pkl   # Trained model (generated)
├── src/
│   ├── components/
│   │   ├── Chat.tsx        # Main chat component
│   │   ├── ChatMessage.tsx # Message display component
│   │   └── ChatInput.tsx   # Input component
│   ├── lib/
│   │   └── supabase.ts     # Supabase client
│   └── App.tsx             # Main app
└── README.md
```

## Setup Instructions

### 1. Backend Setup

First, navigate to the backend directory and install Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### 2. Train the Model

Train the neural network on the finance data:

```bash
python model.py
```

This will:
- Process the training data
- Train a neural network (2000 epochs)
- Save the trained model as `finance_model.pkl`
- Display sample Q&A results

### 3. Start the Backend Server

```bash
python app.py
```

The Flask server will start on `http://localhost:5000`

### 4. Frontend Setup

In a new terminal, install frontend dependencies:

```bash
npm install
```

### 5. Start the Frontend

The dev server starts automatically, or you can run:

```bash
npm run dev
```

The React app will be available at `http://localhost:5173`

## How It Works

### Neural Network Architecture

The chatbot uses a simple feedforward neural network:
- **Input Layer**: Bag-of-words representation (vocabulary size)
- **Hidden Layer**: 16 neurons with sigmoid activation
- **Output Layer**: Softmax for intent classification

### Training Process

1. Tokenizes and stems all patterns in the training data
2. Creates bag-of-words vectors for each pattern
3. Uses backpropagation to learn weights
4. Trains for 2000 epochs with learning rate 0.01

### Response Generation

1. User sends a message
2. Message is converted to bag-of-words vector
3. Neural network predicts intent and confidence score
4. Response is randomly selected from intent's response list
5. Conversation is saved to Supabase

## API Endpoints

### POST /api/chat
Send a message to the chatbot
```json
{
  "message": "How do I start investing?"
}
```

Response:
```json
{
  "response": "To start investing, first pay off high-interest debt...",
  "confidence": 0.95,
  "intent": "investing_basics"
}
```

### GET /api/health
Check API status
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### POST /api/retrain
Retrain the model with updated data

## Training Data Topics

The chatbot is trained on:
- Investing basics
- Stocks and bonds
- ETFs and index funds
- Retirement planning (401k, IRA, Roth IRA)
- Emergency funds
- Debt management
- Budgeting
- Credit scores
- Mortgages
- Portfolio diversification
- Compound interest
- Taxes
- Risk tolerance
- Dollar cost averaging

## Database Schema

### Conversations Table
```sql
- id: uuid (primary key)
- message: text (user's message)
- response: text (bot's response)
- confidence: numeric (model confidence)
- intent: text (detected intent)
- session_id: text (session identifier)
- created_at: timestamptz (timestamp)
```

## Customization

### Adding New Topics

1. Edit `backend/training_data.json`
2. Add a new intent with patterns and responses
3. Retrain the model: `python model.py`
4. Restart the Flask server

### Adjusting Model Parameters

In `backend/model.py`, you can adjust:
- `hidden_neurons`: Number of neurons in hidden layer (default: 16)
- `learning_rate`: Learning rate for training (default: 0.01)
- `epochs`: Number of training iterations (default: 2000)
- `threshold`: Minimum confidence threshold (default: 0.25)

## Testing the Model

You can test the model directly:

```python
from model import FinanceChatbot

chatbot = FinanceChatbot()
chatbot.load_model('finance_model.pkl')

response = chatbot.get_response('How do I invest?', 'training_data.json')
print(response)
```

## Production Considerations

For production use, consider:
- Using a more sophisticated NLP model (BERT, GPT)
- Adding user authentication
- Implementing rate limiting
- Using a production WSGI server (gunicorn)
- Adding more training data
- Implementing conversation context memory
- Adding input validation and sanitization

## License

MIT
# chatbot
