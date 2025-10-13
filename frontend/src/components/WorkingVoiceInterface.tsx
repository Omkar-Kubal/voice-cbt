import React, { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Mic, MicOff, Volume2, Brain, MessageSquare } from 'lucide-react';

interface WorkingVoiceInterfaceProps {
  onTextSubmit: (text: string) => void;
  isListening: boolean;
  isProcessing: boolean;
  isSpeaking: boolean;
}

const WorkingVoiceInterface: React.FC<WorkingVoiceInterfaceProps> = ({
  onTextSubmit,
  isListening,
  isProcessing,
  isSpeaking
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [showTextInput, setShowTextInput] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      console.log('Starting audio recording...');
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          sampleRate: 44100,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true
        } 
      });
      
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };
      
      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        console.log('Audio recorded, size:', audioBlob.size, 'bytes');
        
        // For now, we'll show a text input as fallback
        setShowTextInput(true);
        setTranscript('Audio recorded! Please type what you said:');
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorderRef.current.start();
      setIsRecording(true);
      console.log('Recording started');
    } catch (error) {
      console.error('Error starting recording:', error);
      alert('Microphone access denied. Please allow microphone access and try again.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      console.log('Recording stopped');
    }
  };

  const handleTextSubmit = () => {
    if (transcript.trim()) {
      onTextSubmit(transcript);
      setTranscript('');
      setShowTextInput(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleTextSubmit();
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
            onClick={isRecording ? stopRecording : startRecording}
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

        {/* Status and Instructions */}
        <div className="text-center space-y-2">
          {isRecording && (
            <div className="text-blue-400 animate-pulse">
              <Mic className="h-4 w-4 inline mr-2" />
              Recording... Click to stop
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

          {!isRecording && !isProcessing && !isSpeaking && (
            <div className="text-slate-400">
              <p>Click the microphone to start recording</p>
              <p className="text-sm">Your audio will be processed</p>
            </div>
          )}
        </div>

        {/* Text Input Fallback */}
        {showTextInput && (
          <div className="space-y-3 p-4 bg-slate-800 rounded-lg">
            <p className="text-sm text-slate-300">{transcript}</p>
            <div className="flex space-x-2">
              <input
                type="text"
                value={transcript}
                onChange={(e) => setTranscript(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type what you said..."
                className="flex-1 px-3 py-2 bg-slate-700 text-white rounded border border-slate-600 focus:border-blue-500 focus:outline-none"
                autoFocus
              />
              <Button
                onClick={handleTextSubmit}
                disabled={!transcript.trim()}
                className="bg-blue-600 hover:bg-blue-700"
              >
                <MessageSquare className="h-4 w-4 mr-2" />
                Send
              </Button>
            </div>
          </div>
        )}

        {/* Instructions */}
        <div className="text-center text-sm text-slate-400">
          <p>Click the microphone to record your voice</p>
          <p>After recording, you'll be prompted to type what you said</p>
          <p className="text-xs text-slate-500 mt-2">
            This is a fallback method that works without speech recognition
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default WorkingVoiceInterface;
