import { Bot, User } from 'lucide-react';

interface ChatMessageProps {
  message: string;
  isBot: boolean;
  confidence?: number;
}

export default function ChatMessage({ message, isBot, confidence }: ChatMessageProps) {
  return (
    <div className={`flex gap-3 ${isBot ? 'bg-gray-50' : 'bg-white'} p-4 rounded-lg`}>
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isBot ? 'bg-blue-600' : 'bg-gray-600'
      }`}>
        {isBot ? (
          <Bot className="w-5 h-5 text-white" />
        ) : (
          <User className="w-5 h-5 text-white" />
        )}
      </div>
      <div className="flex-1">
        <div className="text-sm font-medium text-gray-900 mb-1">
          {isBot ? 'Finance Bot' : 'You'}
        </div>
        <div className="text-gray-700 leading-relaxed">{message}</div>
        {isBot && confidence && (
          <div className="mt-2 text-xs text-gray-500">
            Confidence: {(confidence * 100).toFixed(1)}%
          </div>
        )}
      </div>
    </div>
  );
}
