import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ProgressIndicator } from "@/components/onboarding/ProgressIndicator";
import { FeelingScreen } from "@/components/onboarding/FeelingScreen";
import { GoalScreen } from "@/components/onboarding/GoalScreen";
import { EmotionScreen } from "@/components/onboarding/EmotionScreen";
import { NameScreen } from "@/components/onboarding/NameScreen";
import { ProvenToHelpScreen } from "@/components/onboarding/ProvenToHelpScreen";
import { DifferentFromChatGPTScreen } from "@/components/onboarding/DifferentFromChatGPTScreen";
import { WhatBringsYouScreen } from "@/components/onboarding/WhatBringsYouScreen";
import { HowDidYouHearScreen } from "@/components/onboarding/HowDidYouHearScreen";
import { SessionTypeScreen } from "@/components/onboarding/SessionTypeScreen";
import { ArrowLeft } from "lucide-react";
import { useUserSessionContext } from "@/components/auth/UserSessionProvider";

interface OnboardingData {
  feeling: string;
  goal: string;
  emotion: string;
  name: string;
  whatBrings: string;
  howHeard: string;
  sessionType: string;
}

const Onboarding = () => {
  const navigate = useNavigate();
  const { user } = useUserSessionContext();
  const [currentStep, setCurrentStep] = useState(1);
  const [onboardingData, setOnboardingData] = useState<OnboardingData>({
    feeling: "",
    goal: "",
    emotion: "",
    name: user?.name || "",
    whatBrings: "",
    howHeard: "",
    sessionType: ""
  });

  const totalSteps = 8;

  // Auto-advance for steps 5 and 6 (no continue buttons)
  useEffect(() => {
    if (currentStep === 5 || currentStep === 6) {
      const timer = setTimeout(() => {
        handleNext();
      }, 3000); // Auto-advance after 3 seconds
      
      return () => clearTimeout(timer);
    }
  }, [currentStep]);

  // Skip name step if user already has a name
  useEffect(() => {
    if (user?.name && currentStep === 4) {
      // User already has a name, skip to next step
      handleNext();
    }
  }, [user?.name, currentStep]);

  // If user is returning (not new), skip onboarding entirely
  useEffect(() => {
    if (user && !user.isNewUser) {
      // Returning user, skip onboarding
      navigate('/app');
    }
  }, [user, navigate]);

  const handleNext = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleFeelingAnswer = (answer: string) => {
    setOnboardingData(prev => ({ ...prev, feeling: answer }));
    handleNext();
  };

  const handleGoalAnswer = (answer: string) => {
    setOnboardingData(prev => ({ ...prev, goal: answer }));
    handleNext();
  };

  const handleEmotionAnswer = (answer: string) => {
    setOnboardingData(prev => ({ ...prev, emotion: answer }));
    handleNext();
  };

  const handleNameAnswer = (answer: string) => {
    setOnboardingData(prev => ({ ...prev, name: answer }));
    handleNext();
  };

  const handleWhatBringsAnswer = (answer: string) => {
    setOnboardingData(prev => ({ ...prev, whatBrings: answer }));
    handleNext();
  };

  const handleHowHeardAnswer = (answer: string) => {
    setOnboardingData(prev => ({ ...prev, howHeard: answer }));
    handleNext();
  };

  const handleSessionTypeSelect = (type: string) => {
    setOnboardingData(prev => ({ ...prev, sessionType: type }));
    
    // Navigate to main app - both voice and text modes are handled in the same component
    navigate("/app");
  };

  const renderCurrentStep = () => {
    switch (currentStep) {
      case 1:
        return <FeelingScreen onAnswer={handleFeelingAnswer} />;
      
      case 2:
        return <GoalScreen onAnswer={handleGoalAnswer} />;
      
      case 3:
        return <EmotionScreen onAnswer={handleEmotionAnswer} />;
      
      case 4:
        return <NameScreen onAnswer={handleNameAnswer} />;
      
      case 5:
        return (
          <div className="relative">
            <ProvenToHelpScreen />
          </div>
        );
      
      case 6:
        return (
          <div className="relative">
            <DifferentFromChatGPTScreen />
          </div>
        );
      
      case 7:
        return <WhatBringsYouScreen onAnswer={handleWhatBringsAnswer} />;
      
      case 8:
        return <SessionTypeScreen onSelect={handleSessionTypeSelect} />;
      
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <ProgressIndicator currentStep={currentStep} totalSteps={totalSteps} />
      
      {/* Back Button */}
      {currentStep > 1 && (
        <div className="fixed top-20 left-6 z-40">
          <Button
            variant="ghost"
            size="icon"
            onClick={handleBack}
            className="rounded-full"
          >
            <ArrowLeft className="h-5 w-5" />
          </Button>
        </div>
      )}

      {/* Current Step Content */}
      <div className="pt-16">
        {renderCurrentStep()}
      </div>
    </div>
  );
};

export default Onboarding;