#!/usr/bin/env python3
"""
Test runner script for Mathtermind.

This script provides a convenient way to run tests for the Mathtermind project.
It supports running all tests, specific test modules, or tests with specific markers.
"""

import sys
import subprocess
import argparse


def run_tests(args):
    """Run the tests with the specified arguments.
    
    Args:
        args: The command-line arguments.
    
    Returns:
        The exit code from pytest.
    """
    # Build the pytest command
    cmd = ["pytest"]
    
    # Add verbosity
    if args.verbose:
        cmd.append("-v")
    
    # Add coverage
    if args.coverage:
        cmd.extend(["--cov=src", "--cov-report=term-missing"])
        if args.html:
            cmd.append("--cov-report=html")
    
    # Add markers
    if args.unit:
        cmd.append("-m unit")
    elif args.integration:
        cmd.append("-m integration")
    elif args.repository:
        cmd.append("-m repository")
    elif args.service:
        cmd.append("-m service")
    elif args.model:
        cmd.append("-m model")
    elif args.ui:
        cmd.append("-m ui")
    
    # Add specific test modules
    if args.module:
        cmd.append(f"src/tests/{args.module}")
    
    # Add specific test file
    if args.file:
        cmd.append(f"src/tests/{args.file}")
    
    # Run the tests
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(" ".join(cmd), shell=True)
    return result.returncode


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Run tests for Mathtermind")
    
    # Add arguments
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase verbosity")
    parser.add_argument("-c", "--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--html", action="store_true", help="Generate HTML coverage report")
    
    # Add test type arguments
    test_type = parser.add_mutually_exclusive_group()
    test_type.add_argument("-u", "--unit", action="store_true", help="Run unit tests")
    test_type.add_argument("-i", "--integration", action="store_true", help="Run integration tests")
    test_type.add_argument("-r", "--repository", action="store_true", help="Run repository tests")
    test_type.add_argument("-s", "--service", action="store_true", help="Run service tests")
    test_type.add_argument("-m", "--model", action="store_true", help="Run model tests")
    test_type.add_argument("--ui", action="store_true", help="Run UI tests")
    
    # Add specific test module or file arguments
    parser.add_argument("--module", help="Run tests in a specific module (e.g., 'db' or 'services')")
    parser.add_argument("--file", help="Run tests in a specific file (e.g., 'db/test_user_repo.py')")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the tests
    sys.exit(run_tests(args))


if __name__ == "__main__":
    main() 