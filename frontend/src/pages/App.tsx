import { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Mic, MicOff, MessageSquare, Send, Volume2 } from 'lucide-react';
import VoiceSphere from '@/components/VoiceSphere';
import TextInput from '@/components/TextInput';
import ChatHistory from '@/components/ChatHistory';

// Types for our conversation state
interface Message {
  id: string;
  type: 'user' | 'system';
  content: string;
  timestamp: Date;
  emotion?: string;
}

interface SessionState {
  isListening: boolean;
  isProcessing: boolean;
  isSpeaking: boolean;
  inputMode: 'voice' | 'text';
  error: string | null;
  connectionStatus: 'connected' | 'disconnected' | 'connecting';
}

const App = () => {
  // State management for the therapy session
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionState, setSessionState] = useState<SessionState>({
    isListening: false,
    isProcessing: false,
    isSpeaking: false,
    inputMode: 'voice', // Default to voice-first
    error: null,
    connectionStatus: 'connecting'
  });

  // Refs for managing speech synthesis and recognition
  const speechSynthesisRef = useRef<SpeechSynthesisUtterance | null>(null);
  const speechRecognitionRef = useRef<SpeechRecognition | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // Initialize speech recognition and check backend connection on component mount
  useEffect(() => {
    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      speechRecognitionRef.current = new SpeechRecognition();
      
      speechRecognitionRef.current.continuous = false;
      speechRecognitionRef.current.interimResults = false;
      speechRecognitionRef.current.lang = 'en-US';

      speechRecognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        handleVoiceInput(transcript);
      };

      speechRecognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setSessionState(prev => ({ 
          ...prev, 
          isListening: false,
          error: `Speech recognition error: ${event.error}`
        }));
      };

      speechRecognitionRef.current.onend = () => {
        setSessionState(prev => ({ ...prev, isListening: false }));
      };
    } else {
      setSessionState(prev => ({ 
        ...prev, 
        error: 'Speech recognition not supported in this browser'
      }));
    }

    // Check backend connection
    checkBackendConnection();
  }, []);

  // Check backend connection status
  const checkBackendConnection = async () => {
    try {
      const response = await fetch('http://localhost:8000/', {
        method: 'GET',
        timeout: 5000
      });
      
      if (response.ok) {
        setSessionState(prev => ({ 
          ...prev, 
          connectionStatus: 'connected',
          error: null
        }));
      } else {
        setSessionState(prev => ({ 
          ...prev, 
          connectionStatus: 'disconnected',
          error: 'Backend server is not responding properly'
        }));
      }
    } catch (error) {
      setSessionState(prev => ({ 
        ...prev, 
        connectionStatus: 'disconnected',
        error: 'Cannot connect to backend server. Please ensure the server is running.'
      }));
    }
  };

  // Handle voice input from speech recognition
  const handleVoiceInput = async (transcript: string) => {
    if (!transcript.trim()) return;

    // Add user message to chat
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: transcript,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);

    // Send to backend and get response
    await sendToBackend(transcript, 'text');
  };

  // Handle text input from text box
  const handleTextInput = async (text: string) => {
    if (!text.trim()) return;

    // Add user message to chat
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: text,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);

    // Send to backend and get response
    await sendToBackend(text, 'text');
  };

  // Send data to backend API
  const sendToBackend = async (content: string, type: 'text' | 'audio') => {
    setSessionState(prev => ({ ...prev, isProcessing: true, error: null }));

    try {
      const requestBody = type === 'audio' 
        ? { audio_data: content } 
        : { text_data: content };

      const response = await fetch('http://localhost:8000/api/v1/session/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Backend service not found. Please check if the server is running.');
        } else if (response.status === 500) {
          throw new Error('Server error. Please try again in a moment.');
        } else {
          throw new Error(`Server error (${response.status}). Please try again.`);
        }
      }

      const data = await response.json();
      
      // Add system response to chat
      const systemMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'system',
        content: data.response_text || data.response || data.message || 'I understand. Can you tell me more?',
        timestamp: new Date(),
        emotion: data.emotion
      };
      setMessages(prev => [...prev, systemMessage]);

      // Speak the response using TTS
      await speakText(systemMessage.content);

      // Clear any previous errors
      setSessionState(prev => ({ ...prev, error: null }));

    } catch (error) {
      console.error('Error sending to backend:', error);
      
      const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred.';
      
      // Update connection status
      setSessionState(prev => ({ 
        ...prev, 
        connectionStatus: 'disconnected',
        error: errorMessage
      }));
      
      // Add error message to chat
      const errorChatMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'system',
        content: 'I apologize, but I encountered an error. Please check your connection and try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorChatMessage]);
    } finally {
      setSessionState(prev => ({ ...prev, isProcessing: false }));
    }
  };

  // Text-to-Speech functionality with female voice
  const speakText = async (text: string): Promise<void> => {
    return new Promise((resolve) => {
      setSessionState(prev => ({ ...prev, isSpeaking: true }));

      // Stop any current speech
      if (speechSynthesisRef.current) {
        speechSynthesis.speak(speechSynthesisRef.current);
      }

      const utterance = new SpeechSynthesisUtterance(text);
      speechSynthesisRef.current = utterance;

      // Try to find a female voice
      const voices = speechSynthesis.getVoices();
      const femaleVoice = voices.find(voice => 
        voice.name.toLowerCase().includes('female') ||
        voice.name.toLowerCase().includes('woman') ||
        voice.name.toLowerCase().includes('samantha') ||
        voice.name.toLowerCase().includes('karen') ||
        voice.name.toLowerCase().includes('susan')
      );

      if (femaleVoice) {
        utterance.voice = femaleVoice;
      }

      utterance.rate = 0.9;
      utterance.pitch = 1.1;
      utterance.volume = 0.8;

      utterance.onend = () => {
        setSessionState(prev => ({ ...prev, isSpeaking: false }));
        resolve();
      };

      utterance.onerror = () => {
        setSessionState(prev => ({ ...prev, isSpeaking: false }));
        resolve();
      };

      speechSynthesis.speak(utterance);
    });
  };

  // Handle voice sphere click
  const handleVoiceSphereClick = async () => {
    if (sessionState.isListening) {
      // Stop listening
      if (speechRecognitionRef.current) {
        speechRecognitionRef.current.stop();
      }
    } else {
      // Start listening
      if (speechRecognitionRef.current) {
        setSessionState(prev => ({ ...prev, isListening: true }));
        speechRecognitionRef.current.start();
      }
    }
  };

  // Toggle between voice and text input modes
  const toggleInputMode = () => {
    setSessionState(prev => ({
      ...prev,
      inputMode: prev.inputMode === 'voice' ? 'text' : 'voice',
      isListening: false
    }));
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b border-slate-700">
        <div className="flex items-center space-x-4">
          <div className="w-10 h-10 bg-yellow-400 rounded-full flex items-center justify-center">
            <span className="text-slate-900 font-bold text-lg">P</span>
          </div>
          <div>
            <h1 className="text-xl font-bold">Voice CBT Session</h1>
            <p className="text-slate-400 text-sm">
              {sessionState.isListening ? 'Listening...' : 
               sessionState.isProcessing ? 'Processing...' :
               sessionState.isSpeaking ? 'Speaking...' : 
               sessionState.connectionStatus === 'connected' ? 'Ready' :
               sessionState.connectionStatus === 'connecting' ? 'Connecting...' :
               'Disconnected'}
            </p>
            {sessionState.error && (
              <p className="text-red-400 text-xs mt-1">
                {sessionState.error}
              </p>
            )}
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          {sessionState.connectionStatus === 'disconnected' && (
            <Button
              onClick={checkBackendConnection}
              variant="outline"
              className="border-red-600 text-red-300 hover:bg-red-900"
            >
              Retry Connection
            </Button>
          )}
          <Button
            onClick={toggleInputMode}
            variant="outline"
            className="border-slate-600 text-slate-300 hover:bg-slate-800"
            disabled={sessionState.connectionStatus === 'disconnected'}
          >
            {sessionState.inputMode === 'voice' ? (
              <>
                <MessageSquare className="w-4 h-4 mr-2" />
                Switch to Text
              </>
            ) : (
              <>
                <Mic className="w-4 h-4 mr-2" />
                Switch to Voice
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat History */}
        <div className="flex-1 overflow-hidden">
          <ChatHistory messages={messages} />
        </div>

        {/* Input Area */}
        <div className="p-6 border-t border-slate-700">
          {sessionState.inputMode === 'voice' ? (
            <div className="flex flex-col items-center space-y-6">
              <VoiceSphere
                isListening={sessionState.isListening}
                isProcessing={sessionState.isProcessing}
                isSpeaking={sessionState.isSpeaking}
                onClick={handleVoiceSphereClick}
                disabled={sessionState.connectionStatus === 'disconnected'}
                aria-label={sessionState.isListening ? 'Stop listening' : 'Start voice input'}
              />
              <p className="text-slate-400 text-center max-w-md">
                {sessionState.isListening 
                  ? 'Speak now... I\'m listening to what you have to say.'
                  : sessionState.isProcessing
                  ? 'Processing your thoughts...'
                  : sessionState.isSpeaking
                  ? 'Let me respond...'
                  : 'Click the sphere to start talking about what\'s on your mind.'}
              </p>
            </div>
          ) : (
            <TextInput
              onSend={handleTextInput}
              disabled={sessionState.isProcessing || sessionState.isSpeaking}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
