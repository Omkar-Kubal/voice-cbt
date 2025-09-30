import { useState } from "react";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";

interface EmotionScreenProps {
  onAnswer: (answer: string) => void;
}

export const EmotionScreen = ({ onAnswer }: EmotionScreenProps) => {
  const [selectedEmotion, setSelectedEmotion] = useState<string>("");

  const emotions = [
    "Sadness",
    "Anger",
    "Disappointment",
    "Overwhelmed"
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-12">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <h2 className="text-4xl font-bold text-foreground text-center">
          which emotion do you want to work on?
        </h2>

        {/* Options List */}
        <RadioGroup value={selectedEmotion} onValueChange={setSelectedEmotion} className="space-y-4">
          {emotions.map((emotion, index) => (
            <div key={index} className="relative">
              <RadioGroupItem 
                value={emotion} 
                id={emotion}
                className="sr-only"
              />
              <Label 
                htmlFor={emotion}
                className={`
                  block w-full p-4 rounded-lg border-2 cursor-pointer text-center transition-colors duration-200
                  ${selectedEmotion === emotion 
                    ? 'bg-primary text-primary-foreground border-primary' 
                    : 'bg-card text-foreground border-border hover:bg-secondary'
                  }
                `}
              >
                {emotion}
              </Label>
            </div>
          ))}
        </RadioGroup>

        {/* Call-to-Action Button */}
        <div className="max-w-sm mx-auto w-full">
          <Button 
            className="btn-hero w-full" 
            disabled={!selectedEmotion}
            onClick={() => selectedEmotion && onAnswer(selectedEmotion)}
          >
            Continue
          </Button>
        </div>
      </div>
    </div>
  );
};