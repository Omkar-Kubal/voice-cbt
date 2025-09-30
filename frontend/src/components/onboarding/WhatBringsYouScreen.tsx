import { useState } from "react";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";

interface WhatBringsYouScreenProps {
  onAnswer: (answer: string) => void;
}

export const WhatBringsYouScreen = ({ onAnswer }: WhatBringsYouScreenProps) => {
  const [selectedOption, setSelectedOption] = useState<string>("");

  const options = [
    "unlock insights about myself",
    "process my emotions", 
    "set and achieve my goals",
    "just need to vent",
    "i don't know yet"
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-12">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <h2 className="text-4xl font-bold text-foreground text-center">
          what brings you to Pravesti?
        </h2>

        {/* Options List */}
        <RadioGroup value={selectedOption} onValueChange={setSelectedOption} className="space-y-4">
          {options.map((option, index) => (
            <div key={index} className="relative">
              <RadioGroupItem 
                value={option} 
                id={option}
                className="sr-only"
              />
              <Label 
                htmlFor={option}
                className={`
                  block w-full p-4 rounded-lg border-2 cursor-pointer text-center transition-colors duration-200
                  ${selectedOption === option 
                    ? 'bg-primary text-primary-foreground border-primary' 
                    : 'bg-card text-foreground border-border hover:bg-secondary'
                  }
                `}
              >
                {option}
              </Label>
            </div>
          ))}
        </RadioGroup>

        {/* Call-to-Action Button */}
        <div className="max-w-sm mx-auto w-full">
          <Button 
            className="btn-hero w-full" 
            disabled={!selectedOption}
            onClick={() => selectedOption && onAnswer(selectedOption)}
          >
            Continue
          </Button>
        </div>
      </div>
    </div>
  );
};