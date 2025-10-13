import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Mic, MicOff, Volume2, Brain } from 'lucide-react';

interface SimpleVoiceInterfaceProps {
  onTextSubmit: (text: string) => void;
  isListening: boolean;
  isProcessing: boolean;
  isSpeaking: boolean;
}

const SimpleVoiceInterface: React.FC<SimpleVoiceInterfaceProps> = ({
  onTextSubmit,
  isListening,
  isProcessing,
  isSpeaking
}) => {
  const [transcript, setTranscript] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = 'en-US';
      recognitionRef.current.maxAlternatives = 1;

      recognitionRef.current.onstart = () => {
        console.log('Speech recognition started');
        setIsRecording(true);
      };

      recognitionRef.current.onresult = (event: any) => {
        const current = event.resultIndex;
        const transcript = event.results[current][0].transcript;
        setTranscript(transcript);
        
        if (event.results[current].isFinal) {
          console.log('Final transcript:', transcript);
          onTextSubmit(transcript);
          setTranscript('');
        }
      };

      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        setIsRecording(false);
        
        // Handle specific error types
        if (event.error === 'network') {
          console.log('Network error - speech recognition requires stable internet connection');
          console.log('Please try again or use text mode instead');
        } else if (event.error === 'not-allowed') {
          console.log('Microphone access denied - please allow microphone access');
        } else if (event.error === 'no-speech') {
          console.log('No speech detected - try speaking louder');
        } else if (event.error === 'aborted') {
          console.log('Speech recognition aborted');
        }
      };

      recognitionRef.current.onend = () => {
        console.log('Speech recognition ended');
        setIsRecording(false);
      };
    } else {
      console.error('Speech recognition not supported in this browser');
    }
  }, [onTextSubmit]);

  const startListening = () => {
    console.log('Start listening clicked, isRecording:', isRecording);
    if (recognitionRef.current) {
      setTranscript('');
      try {
        console.log('Starting speech recognition...');
        recognitionRef.current.start();
      } catch (error) {
        console.error('Error starting speech recognition:', error);
        setIsRecording(false);
      }
    } else {
      console.error('Speech recognition not available');
    }
  };

  const stopListening = () => {
    console.log('Stopping speech recognition...');
    if (recognitionRef.current && isRecording) {
      try {
        recognitionRef.current.stop();
        setIsRecording(false);
      } catch (error) {
        console.error('Error stopping speech recognition:', error);
        setIsRecording(false);
      }
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Brain className="h-5 w-5" />
          <span>Voice Interface</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Voice Controls */}
        <div className="flex items-center justify-center space-x-4">
          <Button
            onClick={() => {
              console.log('Microphone button clicked! isRecording:', isRecording);
              if (isRecording) {
                stopListening();
              } else {
                startListening();
              }
            }}
            disabled={isProcessing || isSpeaking}
            className={`w-16 h-16 rounded-full ${
              isRecording 
                ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
                : 'bg-blue-500 hover:bg-blue-600'
            }`}
          >
            {isRecording ? <MicOff className="h-8 w-8" /> : <Mic className="h-8 w-8" />}
          </Button>
        </div>

        {/* Status and Transcript */}
        <div className="text-center space-y-2">
          {isRecording && (
            <div className="text-blue-400 animate-pulse">
              <Mic className="h-4 w-4 inline mr-2" />
              Listening... Speak now
            </div>
          )}
          
          {transcript && (
            <div className="p-3 bg-slate-800 rounded-lg">
              <p className="text-sm text-slate-300">You said:</p>
              <p className="text-white font-medium">{transcript}</p>
            </div>
          )}

          {isProcessing && (
            <div className="text-yellow-400 animate-pulse">
              <Brain className="h-4 w-4 inline mr-2" />
              Processing your message...
            </div>
          )}

          {isSpeaking && (
            <div className="text-green-400 animate-pulse">
              <Volume2 className="h-4 w-4 inline mr-2" />
              AI is speaking...
            </div>
          )}
        </div>

        {/* Instructions */}
        <div className="text-center text-sm text-slate-400">
          <p>Click the microphone to start speaking</p>
          <p>Your speech will be converted to text and sent to the AI</p>
          <p className="text-xs text-slate-500 mt-2">
            Note: Speech recognition requires internet connection and works best in Chrome
          </p>
          <p className="text-xs text-slate-500">
            If voice doesn't work, try switching to text mode
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default SimpleVoiceInterface;
