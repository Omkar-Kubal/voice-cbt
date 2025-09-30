import { Button } from "@/components/ui/button";

export const ProvenToHelpScreen = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-12">
      <div className="max-w-md w-full space-y-8 text-center">
        {/* Header */}
        <h2 className="text-4xl font-bold text-foreground">
          proven to help
        </h2>

        {/* Illustration Placeholder */}
        <div className="bg-brand-blue/30 rounded-2xl h-48 w-full flex items-center justify-center">
          <span className="text-6xl">📊</span>
        </div>

        {/* Descriptive Paragraph */}
        <p className="text-lg text-muted-foreground leading-relaxed">
          in a recent study, ai therapy lead to a{" "}
          <span className="font-semibold text-foreground">51%</span> drop in depression and a{" "}
          <span className="font-semibold text-foreground">31%</span> drop in anxiety
        </p>

        {/* Call-to-Action Button */}
        <div className="max-w-sm mx-auto w-full">
          <Button className="btn-hero w-full">
            Continue
          </Button>
        </div>
      </div>
    </div>
  );
};