#!/usr/bin/env python3
"""
Comprehensive Project Validation Script
Tests all components of the Voice CBT project before deployment
"""

import os
import sys
import subprocess
import json
import sqlite3
from pathlib import Path
import importlib.util

class ProjectValidator:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.backend_dir = self.root_dir / "backend"
        self.frontend_dir = self.root_dir / "frontend"
        self.errors = []
        self.warnings = []
        self.success_count = 0
        
    def log_success(self, message):
        print(f"[SUCCESS] {message}")
        self.success_count += 1
        
    def log_error(self, message):
        print(f"[ERROR] {message}")
        self.errors.append(message)
        
    def log_warning(self, message):
        print(f"[WARNING] {message}")
        self.warnings.append(message)
        
    def run_command(self, command, cwd=None, capture_output=True):
        """Run a command and return the result"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=cwd, 
                capture_output=capture_output, 
                text=True,
                timeout=60
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def validate_python_environment(self):
        """Validate Python environment and dependencies"""
        print("\n[CHECK] Validating Python Environment...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version >= (3, 8):
            self.log_success(f"Python version {python_version.major}.{python_version.minor} is supported")
        else:
            self.log_error(f"Python version {python_version.major}.{python_version.minor} is too old. Need 3.8+")
            
        # Check if we can import key modules
        key_modules = ['fastapi', 'uvicorn', 'sqlalchemy', 'pytest']
        for module in key_modules:
            try:
                __import__(module)
                self.log_success(f"Module {module} is available")
            except ImportError:
                self.log_error(f"Module {module} is missing")
    
    def validate_backend_structure(self):
        """Validate backend file structure"""
        print("\n[CHECK] Validating Backend Structure...")
        
        required_files = [
            "app/main.py",
            "app/models/database.py",
            "app/api/audio.py",
            "app/services/llm_integration.py",
            "requirements.txt",
            "config.env"
        ]
        
        for file_path in required_files:
            full_path = self.backend_dir / file_path
            if full_path.exists():
                self.log_success(f"Backend file exists: {file_path}")
            else:
                self.log_error(f"Missing backend file: {file_path}")
    
    def validate_frontend_structure(self):
        """Validate frontend file structure"""
        print("\n[CHECK] Validating Frontend Structure...")
        
        required_files = [
            "package.json",
            "src/main.tsx",
            "src/App.tsx",
            "vite.config.ts"
        ]
        
        for file_path in required_files:
            full_path = self.frontend_dir / file_path
            if full_path.exists():
                self.log_success(f"Frontend file exists: {file_path}")
            else:
                self.log_error(f"Missing frontend file: {file_path}")
    
    def validate_database(self):
        """Validate database connection and structure"""
        print("\n[CHECK] Validating Database...")
        
        db_path = self.backend_dir / "voice_cbt.db"
        if db_path.exists():
            self.log_success("Database file exists")
            
            try:
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                conn.close()
                
                if tables:
                    self.log_success(f"Database has {len(tables)} tables")
                else:
                    self.log_warning("Database exists but has no tables")
            except Exception as e:
                self.log_error(f"Database connection failed: {e}")
        else:
            self.log_warning("Database file doesn't exist (will be created on first run)")
    
    def validate_backend_imports(self):
        """Validate that backend can be imported without errors"""
        print("\n[CHECK] Validating Backend Imports...")
        
        try:
            # Add backend to path
            sys.path.insert(0, str(self.backend_dir))
            
            # Test main imports
            from app.main import app
            self.log_success("Backend main module imports successfully")
            
            # Test key services
            from app.services.llm_integration import LLMIntegration
            self.log_success("LLM integration imports successfully")
            
            from app.services.audio_processor import AudioProcessor
            self.log_success("Audio processor imports successfully")
            
        except Exception as e:
            self.log_error(f"Backend import failed: {e}")
    
    def validate_frontend_build(self):
        """Validate frontend can build successfully"""
        print("\n[CHECK] Validating Frontend Build...")
        
        # Check if node_modules exists
        node_modules = self.frontend_dir / "node_modules"
        if not node_modules.exists():
            self.log_warning("node_modules not found, running npm install...")
            success, stdout, stderr = self.run_command("npm install", cwd=self.frontend_dir)
            if success:
                self.log_success("npm install completed")
            else:
                self.log_error(f"npm install failed: {stderr}")
                return
        
        # Try to build
        success, stdout, stderr = self.run_command("npm run build", cwd=self.frontend_dir)
        if success:
            self.log_success("Frontend builds successfully")
            
            # Check if dist folder was created
            dist_folder = self.frontend_dir / "dist"
            if dist_folder.exists():
                self.log_success("Build output directory created")
            else:
                self.log_warning("Build completed but no dist folder found")
        else:
            self.log_error(f"Frontend build failed: {stderr}")
    
    def validate_docker_setup(self):
        """Validate Docker configuration"""
        print("\n[CHECK] Validating Docker Setup...")
        
        # Check if Docker is available
        success, stdout, stderr = self.run_command("docker --version")
        if success:
            self.log_success("Docker is available")
        else:
            self.log_warning("Docker not available - skipping Docker tests")
            return
        
        # Check docker-compose file
        compose_file = self.root_dir / "docker-compose.simple.yml"
        if compose_file.exists():
            self.log_success("Docker compose file exists")
        else:
            self.log_error("Docker compose file missing")
    
    def validate_config_files(self):
        """Validate configuration files"""
        print("\n[CHECK] Validating Configuration Files...")
        
        # Check backend config
        config_file = self.backend_dir / "config.env"
        if config_file.exists():
            self.log_success("Backend config file exists")
            
            # Check for required environment variables
            with open(config_file, 'r') as f:
                content = f.read()
                if 'OPENAI_API_KEY' in content or 'GEMINI_API_KEY' in content:
                    self.log_success("API keys configured")
                else:
                    self.log_warning("No API keys found in config")
        else:
            self.log_error("Backend config file missing")
        
        # Check frontend config
        package_json = self.frontend_dir / "package.json"
        if package_json.exists():
            self.log_success("Frontend package.json exists")
            try:
                with open(package_json, 'r') as f:
                    data = json.load(f)
                    if 'scripts' in data and 'build' in data['scripts']:
                        self.log_success("Frontend build script configured")
            except json.JSONDecodeError:
                self.log_error("Invalid package.json format")
    
    def run_backend_tests(self):
        """Run backend tests"""
        print("\n[CHECK] Running Backend Tests...")
        
        success, stdout, stderr = self.run_command("python -m pytest tests/ -v", cwd=self.backend_dir)
        if success:
            self.log_success("Backend tests passed")
        else:
            self.log_error(f"Backend tests failed: {stderr}")
    
    def validate_git_status(self):
        """Validate git repository status"""
        print("\n[CHECK] Validating Git Status...")
        
        success, stdout, stderr = self.run_command("git status --porcelain")
        if success:
            if stdout.strip():
                self.log_warning("Uncommitted changes detected")
                print("Uncommitted files:")
                for line in stdout.strip().split('\n'):
                    print(f"  {line}")
            else:
                self.log_success("Working directory is clean")
        else:
            self.log_warning("Not a git repository or git not available")
    
    def generate_report(self):
        """Generate final validation report"""
        print("\n" + "="*60)
        print("VALIDATION REPORT")
        print("="*60)
        
        print(f"Successful checks: {self.success_count}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Errors: {len(self.errors)}")
        
        if self.warnings:
            print("\nWARNINGS:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if self.errors:
            print("\nERRORS:")
            for error in self.errors:
                print(f"  - {error}")
        
        print("\n" + "="*60)
        
        if self.errors:
            print("DEPLOYMENT NOT RECOMMENDED - Fix errors first!")
            return False
        elif self.warnings:
            print("DEPLOYMENT READY with warnings - Review warnings")
            return True
        else:
            print("DEPLOYMENT READY - All checks passed!")
            return True
    
    def run_all_validations(self):
        """Run all validation checks"""
        print("Starting Voice CBT Project Validation")
        print("="*60)
        
        self.validate_python_environment()
        self.validate_backend_structure()
        self.validate_frontend_structure()
        self.validate_database()
        self.validate_backend_imports()
        self.validate_frontend_build()
        self.validate_docker_setup()
        self.validate_config_files()
        self.run_backend_tests()
        self.validate_git_status()
        
        return self.generate_report()

if __name__ == "__main__":
    validator = ProjectValidator()
    success = validator.run_all_validations()
    sys.exit(0 if success else 1)
