import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import Navbar from '@/components/Navbar';

const Index = () => {
  const navigate = useNavigate();
  const [visibleSections, setVisibleSections] = useState<Set<string>>(new Set());

  useEffect(() => {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const sectionId = entry.target.id;
        if (entry.isIntersecting) {
          setVisibleSections(prev => new Set([...prev, sectionId]));
        }
      });
    }, observerOptions);

    // Observe all scroll-reveal sections
    document.querySelectorAll('.scroll-reveal').forEach((section) => {
      observer.observe(section);
    });

    return () => observer.disconnect();
  }, []);

  const features = [
    {
      icon: "🧠",
      title: "Emotionally Intelligent AI",
      description: "Advanced emotion recognition that adapts conversations to your current emotional state and needs."
    },
    {
      icon: "💬",
      title: "Adaptive Conversations",
      description: "Dynamic dialogue that evolves based on your responses, creating personalized therapeutic experiences."
    },
    {
      icon: "📊",
      title: "Progress Tracking",
      description: "Monitor your emotional journey with insightful analytics and mood pattern recognition."
    },
    {
      icon: "🎯",
      title: "Personalized Therapy",
      description: "Tailored CBT techniques that match your unique personality and therapeutic goals."
    },
    {
      icon: "🔐",
      title: "Privacy First",
      description: "Your conversations are encrypted and private. We never store or share your personal data."
    },
    {
      icon: "⚡",
      title: "Available 24/7",
      description: "Get support whenever you need it, with no appointments or waiting times required."
    }
  ];

  const steps = [
    {
      number: "01",
      title: "Start Speaking",
      description: "Simply start talking about what's on your mind. No specific prompts or questions needed.",
      color: "bg-brand-yellow"
    },
    {
      number: "02", 
      title: "AI Listens & Adapts",
      description: "Our AI analyzes your emotions and adapts the conversation to provide personalized support.",
      color: "bg-brand-blue"
    },
    {
      number: "03",
      title: "Explore Together",
      description: "Work through your thoughts and emotions with guided CBT techniques and insights.",
      color: "bg-brand-purple"
    },
    {
      number: "04",
      title: "Track Progress",
      description: "Monitor your emotional patterns and celebrate your growth over time.",
      color: "bg-brand-green"
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-secondary/30 to-accent/10">
        <div className="container mx-auto px-6 text-center">
          <div className="max-w-4xl mx-auto space-y-8">
            <h1 className="text-5xl md:text-7xl font-black text-foreground leading-tight">
              It's not therapy.
              <br />
              <span className="text-gradient">It's just Voice CBT.</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              Your wise, witty AI built to help you explore your thoughts, emotions, and behaviors through natural conversation.
            </p>
            
            <div className="space-y-6">
              <Button 
                size="lg" 
                className="btn-hero text-lg px-12 py-6 rounded-2xl"
                onClick={() => {
                  // Check if user is logged in
                  const user = JSON.parse(localStorage.getItem('voice_cbt_user') || 'null');
                  const session = localStorage.getItem('voice_cbt_session');
                  
                  if (user && session === 'active') {
                    // User is logged in, check if they're new or returning
                    if (user.isNewUser) {
                      navigate('/onboarding');
                    } else {
                      navigate('/app');
                    }
                  } else {
                    // User not logged in, go to login
                    navigate('/login');
                  }
                }}
              >
                Start Yapping — it's free
              </Button>
              
              <p className="text-muted-foreground">
                💖 loved by <span className="font-semibold text-foreground">100,000+ cool people</span>
              </p>
            </div>
          </div>
        </div>
        
        {/* Floating elements for visual interest */}
        <div className="absolute top-1/4 left-10 w-20 h-20 bg-brand-yellow/20 rounded-full blur-xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-10 w-32 h-32 bg-brand-blue/20 rounded-full blur-xl animate-pulse delay-1000"></div>
      </section>

      {/* What is Voice CBT Section */}
      <section id="about" className={`py-20 bg-secondary/30 scroll-reveal ${visibleSections.has('about') ? 'revealed' : ''}`}>
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            <h2 className="text-4xl md:text-5xl font-bold text-foreground">
              What is Voice CBT?
            </h2>
            <p className="text-lg md:text-xl text-muted-foreground leading-relaxed">
              Voice CBT combines the proven effectiveness of Cognitive Behavioral Therapy with 
              advanced AI that understands not just your words, but your emotions. Unlike traditional 
              text-based therapy apps, our voice-first approach creates more natural, intuitive 
              conversations that adapt to your emotional state in real-time.
            </p>
            <div className="grid md:grid-cols-3 gap-8 mt-16">
              <div className="text-center space-y-4">
                <div className="w-16 h-16 mx-auto bg-accent rounded-2xl flex items-center justify-center text-2xl">
                  🎙️
                </div>
                <h3 className="text-xl font-bold">Voice-First</h3>
                <p className="text-muted-foreground">Natural conversation feels more authentic than typing</p>
              </div>
              <div className="text-center space-y-4">
                <div className="w-16 h-16 mx-auto bg-brand-blue rounded-2xl flex items-center justify-center text-2xl">
                  🤖
                </div>
                <h3 className="text-xl font-bold">AI-Powered</h3>
                <p className="text-muted-foreground">Advanced algorithms that understand emotional context</p>
              </div>
              <div className="text-center space-y-4">
                <div className="w-16 h-16 mx-auto bg-brand-purple rounded-2xl flex items-center justify-center text-2xl">
                  🧘
                </div>
                <h3 className="text-xl font-bold">CBT-Based</h3>
                <p className="text-muted-foreground">Grounded in proven therapeutic techniques</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className={`py-20 scroll-reveal ${visibleSections.has('features') ? 'revealed' : ''}`}>
        <div className="container mx-auto px-6">
          <div className="text-center space-y-8 mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-foreground">
              How It Helps You
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Discover the powerful features that make Voice CBT your perfect therapeutic companion.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card 
                key={index} 
                className={`feature-card border-0 bg-gradient-to-br from-card to-secondary/50 scroll-reveal ${
                  visibleSections.has('features') ? 'revealed' : ''
                }`}
                style={{ transitionDelay: `${index * 100}ms` }}
              >
                <CardContent className="p-8 text-center space-y-4">
                  <div className="text-4xl mb-4">{feature.icon}</div>
                  <h3 className="text-xl font-bold text-foreground">{feature.title}</h3>
                  <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className={`py-20 bg-gradient-to-br from-secondary/30 to-accent/5 scroll-reveal ${visibleSections.has('how-it-works') ? 'revealed' : ''}`}>
        <div className="container mx-auto px-6">
          <div className="text-center space-y-8 mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-foreground">
              How Voice CBT Works
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Four simple steps to start your journey toward better mental health.
            </p>
          </div>
          
          <div className="max-w-6xl mx-auto">
            {steps.map((step, index) => (
              <div 
                key={index} 
                className={`flex flex-col md:flex-row items-center gap-8 mb-16 scroll-reveal ${
                  visibleSections.has('how-it-works') ? 'revealed' : ''
                } ${index % 2 === 1 ? 'md:flex-row-reverse' : ''}`}
                style={{ transitionDelay: `${index * 200}ms` }}
              >
                <div className="flex-1 space-y-6">
                  <div className="flex items-center space-x-4">
                    <div className={`w-12 h-12 ${step.color} rounded-xl flex items-center justify-center text-white font-bold text-lg`}>
                      {step.number}
                    </div>
                    <h3 className="text-2xl font-bold text-foreground">{step.title}</h3>
                  </div>
                  <p className="text-lg text-muted-foreground leading-relaxed">
                    {step.description}
                  </p>
                </div>
                <div className="flex-1 flex justify-center">
                  <div className={`w-64 h-64 ${step.color}/20 rounded-3xl flex items-center justify-center`}>
                    <div className={`w-32 h-32 ${step.color} rounded-2xl flex items-center justify-center text-4xl text-white`}>
                      {step.number}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className={`py-20 bg-gradient-to-r from-accent to-brand-blue scroll-reveal ${visibleSections.has('cta') ? 'revealed' : ''}`} id="cta">
        <div className="container mx-auto px-6 text-center">
          <div className="max-w-3xl mx-auto space-y-8">
            <h2 className="text-4xl md:text-5xl font-bold text-white">
              Ready to Start Your Journey?
            </h2>
            <p className="text-xl text-white/90 leading-relaxed">
              Join thousands of people who have transformed their mental health with Voice CBT.
              Your first session is completely free.
            </p>
            <Button 
              size="lg" 
              className="bg-white text-foreground hover:bg-white/90 font-semibold px-12 py-6 rounded-2xl text-lg"
            >
              Start Yapping Today
            </Button>
          </div>
        </div>
      </section>

      {/* Disclaimer Section */}
      <section className={`py-16 bg-muted/50 scroll-reveal ${visibleSections.has('disclaimer') ? 'revealed' : ''}`} id="disclaimer">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto text-center space-y-6">
            <h3 className="text-2xl font-bold text-foreground">Important Disclaimer</h3>
            <p className="text-muted-foreground leading-relaxed">
              Voice CBT is designed to complement, not replace, professional mental health care. 
              While our AI provides valuable support and CBT-based techniques, it's not a substitute 
              for therapy with a licensed professional. If you're experiencing severe mental health 
              concerns, thoughts of self-harm, or crisis situations, please contact a mental health 
              professional or emergency services immediately.
            </p>
            <div className="flex flex-wrap justify-center gap-4 text-sm text-muted-foreground">
              <span>🔒 Privacy Protected</span>
              <span>•</span>
              <span>🎓 Evidence-Based</span>
              <span>•</span>
              <span>⚡ Available 24/7</span>
              <span>•</span>
              <span>🌟 Trusted by Thousands</span>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-foreground text-background">
        <div className="container mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center">
                <span className="text-accent-foreground font-bold text-lg">P</span>
              </div>
              <span className="text-xl font-bold">Pravesti</span>
            </div>
            <div className="flex items-center space-x-6 text-sm">
              <a href="#" className="hover:text-accent transition-colors">Privacy Policy</a>
              <a href="#" className="hover:text-accent transition-colors">Terms of Service</a>
              <a href="#" className="hover:text-accent transition-colors">License</a>
            </div>
            <p className="text-sm text-muted">
              © 2024 Pravesti. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
