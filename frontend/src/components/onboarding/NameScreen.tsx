import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface NameScreenProps {
  onAnswer: (answer: string) => void;
}

export const NameScreen = ({ onAnswer }: NameScreenProps) => {
  const [name, setName] = useState<string>("");

  const handleSubmit = () => {
    if (name.trim()) {
      onAnswer(name.trim());
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-12">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <h2 className="text-4xl font-bold text-foreground text-center">
          it's a pleasure to meet you. what's your name?
        </h2>

        {/* Input Field */}
        <div className="space-y-4">
          <Input
            type="text"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            onKeyPress={handleKeyPress}
            className="w-full p-4 text-center text-lg"
            autoFocus
          />
        </div>

        {/* Call-to-Action Button */}
        <div className="max-w-sm mx-auto w-full">
          <Button 
            className="btn-hero w-full" 
            disabled={!name.trim()}
            onClick={handleSubmit}
          >
            Continue
          </Button>
        </div>
      </div>
    </div>
  );
};