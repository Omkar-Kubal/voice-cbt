import { useState } from "react";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";

interface FeelingScreenProps {
  onAnswer: (answer: string) => void;
}

export const FeelingScreen = ({ onAnswer }: FeelingScreenProps) => {
  const [selectedFeeling, setSelectedFeeling] = useState<string>("");

  const feelings = [
    "Anxious",
    "Stressed", 
    "Sad",
    "Calm",
    "Happy"
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-12">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <h2 className="text-4xl font-bold text-foreground text-center">
          how are you feeling right now?
        </h2>

        {/* Options List */}
        <RadioGroup value={selectedFeeling} onValueChange={setSelectedFeeling} className="space-y-4">
          {feelings.map((feeling, index) => (
            <div key={index} className="relative">
              <RadioGroupItem 
                value={feeling} 
                id={feeling}
                className="sr-only"
              />
              <Label 
                htmlFor={feeling}
                className={`
                  block w-full p-4 rounded-lg border-2 cursor-pointer text-center transition-colors duration-200
                  ${selectedFeeling === feeling 
                    ? 'bg-primary text-primary-foreground border-primary' 
                    : 'bg-card text-foreground border-border hover:bg-secondary'
                  }
                `}
              >
                {feeling}
              </Label>
            </div>
          ))}
        </RadioGroup>

        {/* Call-to-Action Button */}
        <div className="max-w-sm mx-auto w-full">
          <Button 
            className="btn-hero w-full" 
            disabled={!selectedFeeling}
            onClick={() => selectedFeeling && onAnswer(selectedFeeling)}
          >
            Continue
          </Button>
        </div>
      </div>
    </div>
  );
};