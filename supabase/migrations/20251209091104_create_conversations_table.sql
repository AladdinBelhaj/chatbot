/*
  # Create conversations table for finance chatbot

  1. New Tables
    - `conversations`
      - `id` (uuid, primary key)
      - `message` (text) - The user's message
      - `response` (text) - The bot's response
      - `confidence` (numeric) - Model confidence score
      - `intent` (text) - Detected intent/tag
      - `created_at` (timestamptz) - When the conversation occurred
      - `session_id` (text) - To group conversations by session

  2. Security
    - Enable RLS on `conversations` table
    - Add policy for public insert access (anyone can log conversations)
    - Add policy for public read access (anyone can view conversation history)

  Note: In a production app, you'd want to tie this to authenticated users
*/

CREATE TABLE IF NOT EXISTS conversations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  message text NOT NULL,
  response text NOT NULL,
  confidence numeric,
  intent text,
  session_id text NOT NULL,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public to insert conversations"
  ON conversations
  FOR INSERT
  TO public
  WITH CHECK (true);

CREATE POLICY "Allow public to read conversations"
  ON conversations
  FOR SELECT
  TO public
  USING (true);

CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at DESC);
