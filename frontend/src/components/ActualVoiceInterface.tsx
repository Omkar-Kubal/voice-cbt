import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Mic, MicOff, Volume2, Brain, Loader2 } from 'lucide-react';

interface ActualVoiceInterfaceProps {
  onTextSubmit: (text: string) => void;
  isListening: boolean;
  isProcessing: boolean;
  isSpeaking: boolean;
}

const ActualVoiceInterface: React.FC<ActualVoiceInterfaceProps> = ({
  onTextSubmit,
  isListening,
  isProcessing,
  isSpeaking
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isProcessingAudio, setIsProcessingAudio] = useState(false);
  const [error, setError] = useState('');
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
        setError('');
      };

      recognitionRef.current.onresult = (event: any) => {
        const current = event.resultIndex;
        const transcript = event.results[current][0].transcript;
        setTranscript(transcript);
        
        if (event.results[current].isFinal) {
          console.log('Final transcript:', transcript);
          // Automatically submit the transcript
          onTextSubmit(transcript);
          setTranscript('');
        }
      };

      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        setIsRecording(false);
        setError(`Speech recognition error: ${event.error}`);
      };

      recognitionRef.current.onend = () => {
        console.log('Speech recognition ended');
        setIsRecording(false);
      };
    } else {
      setError('Speech recognition not supported in this browser');
    }
  }, [onTextSubmit]);

  const startListening = () => {
    console.log('Start listening clicked');
    if (recognitionRef.current) {
      setTranscript('');
      setError('');
      try {
        recognitionRef.current.start();
      } catch (error) {
        console.error('Error starting speech recognition:', error);
        setError('Error starting speech recognition');
      }
    } else {
      setError('Speech recognition not available');
    }
  };

  const stopListening = () => {
    console.log('Stop listening clicked');
    if (recognitionRef.current && isRecording) {
      recognitionRef.current.stop();
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Brain className="h-5 w-5" />
          <span>Real Voice Interface</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Voice Controls */}
        <div className="flex items-center justify-center space-x-4">
          <Button
            onClick={isRecording ? stopListening : startListening}
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
          
          {isProcessing && (
            <div className="text-yellow-400 animate-pulse">
              <Brain className="h-4 w-4 inline mr-2" />
              AI is thinking...
            </div>
          )}

          {isSpeaking && (
            <div className="text-green-400 animate-pulse">
              <Volume2 className="h-4 w-4 inline mr-2" />
              AI is speaking...
            </div>
          )}

          {transcript && (
            <div className="p-3 bg-slate-800 rounded-lg">
              <p className="text-sm text-slate-300">You said:</p>
              <p className="text-white font-medium">{transcript}</p>
            </div>
          )}

          {error && (
            <div className="p-3 bg-red-900 border border-red-600 rounded-lg">
              <p className="text-red-300 text-sm">{error}</p>
            </div>
          )}

          {!isRecording && !isProcessing && !isSpeaking && !transcript && !error && (
            <div className="text-slate-400">
              <p>Click the microphone to start speaking</p>
              <p className="text-sm">Your speech will be converted to text automatically</p>
            </div>
          )}
        </div>

        {/* Instructions */}
        <div className="text-center text-sm text-slate-400">
          <p>Click the microphone and speak naturally</p>
          <p>Your speech will be converted to text and sent to the AI</p>
          <p className="text-xs text-slate-500 mt-2">
            Uses browser's built-in speech recognition
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default ActualVoiceInterface;
