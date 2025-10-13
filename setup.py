#!/usr/bin/env python3
"""
Voice CBT Setup Script
Simple setup for the Voice CBT application
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_step(step, message):
    """Print a setup step with formatting"""
    print(f"\n{'='*50}")
    print(f"Step {step}: {message}")
    print(f"{'='*50}")

def check_docker():
    """Check if Docker is installed and running"""
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✓ Docker found: {result.stdout.strip()}")
        
        result = subprocess.run(['docker-compose', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✓ Docker Compose found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Docker or Docker Compose not found!")
        print("Please install Docker Desktop from: https://www.docker.com/products/docker-desktop")
        return False

def check_environment():
    """Check and setup environment files"""
    config_file = Path("backend/config.env")
    example_file = Path("backend/config.env.example")
    
    if not config_file.exists():
        if example_file.exists():
            shutil.copy(example_file, config_file)
            print("✓ Created config.env from example")
        else:
            print("✗ config.env.example not found!")
            return False
    
    # Check for required environment variables
    with open(config_file, 'r') as f:
        content = f.read()
        
    if "OPENAI_API_KEY=your-api-key-here" in content:
        print("⚠️  Please add your OpenAI API key to backend/config.env")
        print("   Edit the file and replace 'your-api-key-here' with your actual API key")
        return False
    
    print("✓ Environment configuration looks good")
    return True

def setup_directories():
    """Create necessary directories"""
    directories = [
        "backend/data",
        "backend/logs", 
        "backend/trained_models"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def start_services():
    """Start Docker services"""
    print("\nStarting Voice CBT services...")
    try:
        # Stop any existing services
        subprocess.run(['docker-compose', '-f', 'docker-compose.simple.yml', 'down'], 
                      check=False, capture_output=True)
        
        # Start services
        result = subprocess.run(['docker-compose', '-f', 'docker-compose.simple.yml', 'up', '--build', '-d'], 
                              check=True, capture_output=True, text=True)
        print("✓ Services started successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to start services: {e}")
        print(f"Error output: {e.stderr}")
        return False

def show_access_info():
    """Show how to access the application"""
    print("\n" + "="*60)
    print("🎉 Voice CBT Setup Complete!")
    print("="*60)
    print("\n📱 Access your application:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    
    print("\n🔧 Useful commands:")
    print("   View logs: docker-compose -f docker-compose.simple.yml logs -f")
    print("   Stop services: docker-compose -f docker-compose.simple.yml down")
    print("   Restart: docker-compose -f docker-compose.simple.yml restart")
    
    print("\n📚 Next steps:")
    print("   1. Open http://localhost:3000 in your browser")
    print("   2. Set up Firebase authentication (see AUTHENTICATION_SETUP.md)")
    print("   3. Start using the Voice CBT application!")
    
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("🚀 Voice CBT Setup Script")
    print("Setting up your AI-powered therapeutic assistant...")
    
    # Step 1: Check Docker
    print_step(1, "Checking Docker Installation")
    if not check_docker():
        sys.exit(1)
    
    # Step 2: Setup environment
    print_step(2, "Setting up Environment")
    if not check_environment():
        print("\n⚠️  Please configure your environment variables and run this script again.")
        sys.exit(1)
    
    # Step 3: Create directories
    print_step(3, "Creating Directories")
    setup_directories()
    
    # Step 4: Start services
    print_step(4, "Starting Services")
    if not start_services():
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
    
    # Step 5: Show access information
    show_access_info()

if __name__ == "__main__":
    main()
