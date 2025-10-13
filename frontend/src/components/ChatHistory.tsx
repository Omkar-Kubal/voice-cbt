import { useEffect, useRef } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { User, Bot, Clock, Heart } from 'lucide-react';

interface Message {
  id: string;
  type: 'user' | 'system';
  content: string;
  timestamp: Date;
  emotion?: string;
}

interface ChatHistoryProps {
  messages: Message[];
}

const ChatHistory = ({ messages }: ChatHistoryProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  // Format timestamp for display
  const formatTime = (timestamp: Date) => {
    try {
      // Ensure timestamp is a valid Date object
      const date = timestamp instanceof Date ? timestamp : new Date(timestamp);
      
      // Check if the date is valid
      if (isNaN(date.getTime())) {
        return 'Invalid time';
      }
      
      return new Intl.DateTimeFormat('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      }).format(date);
    } catch (error) {
      console.error('Error formatting time:', error);
      return 'Invalid time';
    }
  };

  // Get emotion color and icon
  const getEmotionDisplay = (emotion?: string) => {
    if (!emotion) return null;

    const emotionConfig = {
      happy: { color: 'bg-green-500', icon: '😊', label: 'Happy' },
      sad: { color: 'bg-blue-500', icon: '😢', label: 'Sad' },
      angry: { color: 'bg-red-500', icon: '😠', label: 'Angry' },
      anxious: { color: 'bg-yellow-500', icon: '😰', label: 'Anxious' },
      calm: { color: 'bg-purple-500', icon: '😌', label: 'Calm' },
      excited: { color: 'bg-orange-500', icon: '🤩', label: 'Excited' },
      confused: { color: 'bg-gray-500', icon: '😕', label: 'Confused' },
      frustrated: { color: 'bg-red-600', icon: '😤', label: 'Frustrated' }
    };

    const config = emotionConfig[emotion.toLowerCase() as keyof typeof emotionConfig] || 
                  { color: 'bg-slate-500', icon: '💭', label: emotion };

    return (
      <Badge 
        variant="secondary" 
        className={`${config.color} text-white text-xs px-2 py-1`}
      >
        <span className="mr-1">{config.icon}</span>
        {config.label}
      </Badge>
    );
  };

  // Render individual message
  const renderMessage = (message: Message) => {
    const isUser = message.type === 'user';
    
    return (
      <div
        key={message.id}
        className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
      >
        <div className={`flex items-start space-x-3 max-w-[80%] ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
          {/* Avatar */}
          <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
            isUser 
              ? 'bg-yellow-400 text-slate-900' 
              : 'bg-slate-700 text-white'
          }`}>
            {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
          </div>

          {/* Message content */}
          <div className={`flex flex-col space-y-2 ${isUser ? 'items-end' : 'items-start'}`}>
            <Card className={`${
              isUser 
                ? 'bg-yellow-400 text-slate-900 border-yellow-300' 
                : 'bg-slate-800 text-white border-slate-600'
            }`}>
              <CardContent className="p-4">
                <div className="whitespace-pre-wrap break-words">
                  {message.content}
                </div>
              </CardContent>
            </Card>

            {/* Message metadata */}
            <div className={`flex items-center space-x-2 text-xs text-slate-400 ${
              isUser ? 'flex-row-reverse space-x-reverse' : ''
            }`}>
              <div className="flex items-center space-x-1">
                <Clock className="w-3 h-3" />
                <span>{formatTime(message.timestamp)}</span>
              </div>
              
              {/* Emotion indicator for system messages */}
              {!isUser && message.emotion && (
                <div className="flex items-center space-x-1">
                  <Heart className="w-3 h-3" />
                  {getEmotionDisplay(message.emotion)}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Welcome message when no messages
  const renderWelcomeMessage = () => (
    <div className="flex flex-col items-center justify-center h-full text-center space-y-6">
      <div className="w-20 h-20 bg-yellow-400 rounded-full flex items-center justify-center">
        <Heart className="w-10 h-10 text-slate-900" />
      </div>
      <div className="space-y-2">
        <h3 className="text-xl font-semibold text-white">
          Welcome to your therapy session
        </h3>
        <p className="text-slate-400 max-w-md">
          I'm here to listen and help you explore your thoughts and feelings. 
          Whether you want to talk or type, I'm ready to support you.
        </p>
      </div>
      <div className="flex items-center space-x-4 text-sm text-slate-500">
        <span>🔒 Your conversation is private</span>
        <span>•</span>
        <span>💬 Share what's on your mind</span>
        <span>•</span>
        <span>🤖 AI-powered support</span>
      </div>
    </div>
  );

  return (
    <div 
      ref={scrollRef}
      className="flex-1 overflow-y-auto p-6 space-y-4"
      style={{ scrollbarWidth: 'thin' }}
    >
      {messages.length === 0 ? (
        renderWelcomeMessage()
      ) : (
        <div className="space-y-4">
          {messages.map(renderMessage)}
        </div>
      )}
    </div>
  );
};

export default ChatHistory;
