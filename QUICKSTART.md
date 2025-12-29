# Quick Start Guide

Get the Finance AI Chatbot running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- pip (Python package manager)

## Step 1: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 2: Train the Neural Network

```bash
python model.py
```

You should see output like:
```
Training on 100+ samples...
Epoch 200/2000, Loss: 0.1234
...
Training complete!
Model saved to finance_model.pkl
```

## Step 3: Start the Backend

```bash
python app.py
```

Keep this terminal open. The backend runs on `http://localhost:5000`

## Step 4: Start the Frontend

Open a NEW terminal and run:

```bash
npm install   # Only needed first time
npm run dev   # (this may already be running)
```

## Step 5: Chat!

Open your browser and start asking finance questions:
- "How do I start investing?"
- "What is an emergency fund?"
- "Tell me about retirement planning"
- "Should I pay off debt or invest?"

## Troubleshooting

### Backend won't start
- Make sure Python 3.8+ is installed: `python --version`
- Install dependencies: `pip install flask flask-cors numpy`

### Frontend shows "connection error"
- Make sure the backend is running on port 5000
- Check the terminal for error messages

### Model training fails
- Ensure `training_data.json` exists in the `backend/` folder
- Check that NumPy is installed: `pip install numpy`

## What's Happening Behind the Scenes?

1. **Training**: The neural network learns patterns from 100+ finance Q&A examples
2. **Classification**: When you ask a question, it's converted to a bag-of-words vector
3. **Prediction**: The network predicts the intent (topic) with a confidence score
4. **Response**: A relevant response is selected and sent back to you
5. **Storage**: Your conversation is saved to Supabase for analytics

## Next Steps

- Check out `training_data.json` to see what topics the bot knows
- Add your own finance Q&A patterns
- Retrain the model to include your new data
- Adjust model parameters in `model.py` for better accuracy

Enjoy chatting with your AI finance assistant! 💰
