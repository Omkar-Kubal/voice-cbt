#!/usr/bin/env python3
"""
Test runner script for the Voice CBT application.
This script provides a convenient way to run different types of tests.
"""

import sys
import subprocess
import argparse
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("✅ SUCCESS")
        if result.stdout:
            print("STDOUT:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

def install_test_dependencies():
    """Install test dependencies."""
    test_deps = [
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0",
        "pytest-mock>=3.10.0",
        "httpx>=0.24.0",
        "psutil>=5.9.0"
    ]
    
    for dep in test_deps:
        if not run_command([sys.executable, "-m", "pip", "install", dep], f"Installing {dep}"):
            return False
    return True

def run_unit_tests():
    """Run unit tests."""
    return run_command([
        sys.executable, "-m", "pytest", 
        "tests/test_services.py", 
        "-m", "unit",
        "--tb=short"
    ], "Unit Tests")

def run_api_tests():
    """Run API tests."""
    return run_command([
        sys.executable, "-m", "pytest", 
        "tests/test_api_endpoints.py", 
        "-m", "api",
        "--tb=short"
    ], "API Tests")

def run_integration_tests():
    """Run integration tests."""
    return run_command([
        sys.executable, "-m", "pytest", 
        "tests/test_integration.py", 
        "-m", "integration",
        "--tb=short"
    ], "Integration Tests")

def run_all_tests():
    """Run all tests."""
    return run_command([
        sys.executable, "-m", "pytest", 
        "tests/",
        "--tb=short",
        "--durations=10"
    ], "All Tests")

def run_coverage_tests():
    """Run tests with coverage."""
    # Install coverage if not already installed
    run_command([sys.executable, "-m", "pip", "install", "pytest-cov"], "Installing pytest-cov")
    
    return run_command([
        sys.executable, "-m", "pytest", 
        "tests/",
        "--cov=app",
        "--cov-report=html",
        "--cov-report=term-missing",
        "--tb=short"
    ], "Tests with Coverage")

def run_performance_tests():
    """Run performance tests."""
    return run_command([
        sys.executable, "-m", "pytest", 
        "tests/test_integration.py::TestPerformance", 
        "-v",
        "--tb=short"
    ], "Performance Tests")

def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Voice CBT Test Runner")
    parser.add_argument("--type", choices=[
        "unit", "api", "integration", "all", "coverage", "performance"
    ], default="all", help="Type of tests to run")
    parser.add_argument("--install-deps", action="store_true", 
                       help="Install test dependencies")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
    
    args = parser.parse_args()
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    print("🧪 Voice CBT Test Runner")
    print("=" * 60)
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_test_dependencies():
            print("❌ Failed to install test dependencies")
            sys.exit(1)
        print("✅ Test dependencies installed successfully")
    
    # Run tests based on type
    success = False
    
    if args.type == "unit":
        success = run_unit_tests()
    elif args.type == "api":
        success = run_api_tests()
    elif args.type == "integration":
        success = run_integration_tests()
    elif args.type == "all":
        success = run_all_tests()
    elif args.type == "coverage":
        success = run_coverage_tests()
    elif args.type == "performance":
        success = run_performance_tests()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
