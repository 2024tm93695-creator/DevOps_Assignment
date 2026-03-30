#!/usr/bin/env python
"""
Verification script to ensure Pytest integration is complete and working.
Run this from the flask_app directory to validate the test setup.
"""

import os
import sys
import subprocess
from pathlib import Path

class TestSetupVerifier:
    def __init__(self):
        self.base_path = Path.cwd()
        self.issues = []
        self.successes = []

    def check_file_exists(self, path, description):
        """Check if a required file exists."""
        if Path(path).exists():
            self.successes.append(f"✅ {description}: {path}")
            return True
        else:
            self.issues.append(f"❌ Missing: {description} at {path}")
            return False

    def check_directory_exists(self, path, description):
        """Check if a required directory exists."""
        if Path(path).is_dir():
            self.successes.append(f"✅ {description}: {path}")
            return True
        else:
            self.issues.append(f"❌ Missing directory: {description} at {path}")
            return False

    def check_pytest_installed(self):
        """Check if pytest is installed."""
        try:
            import pytest
            self.successes.append(f"✅ Pytest installed: {pytest.__version__}")
            return True
        except ImportError:
            self.issues.append("❌ Pytest not installed. Run: pip install -r requirements.txt")
            return False

    def verify_all(self):
        """Run all verification checks."""
        print("=" * 60)
        print("🧪 PYTEST INTEGRATION VERIFICATION")
        print("=" * 60)
        
        # Check test files
        print("\n📋 Checking Test Files:")
        self.check_file_exists("tests/test_utils.py", "Utility tests")
        self.check_file_exists("tests/test_models.py", "Model tests")
        self.check_file_exists("tests/test_services.py", "Service tests")
        self.check_file_exists("tests/test_routes.py", "Route tests")
        self.check_file_exists("tests/__init__.py", "Test package init")
        
        # Check configuration files
        print("\n⚙️  Checking Configuration Files:")
        self.check_file_exists("conftest.py", "Pytest fixtures")
        self.check_file_exists("pytest.ini", "Pytest configuration")
        self.check_file_exists("requirements.txt", "Dependencies")
        
        # Check CI/CD files
        print("\n🔄 Checking CI/CD Files:")
        self.check_file_exists("../.github/workflows/test.yml", "GitHub Actions")
        self.check_file_exists("../azure-pipelines.yml", "Azure Pipelines")
        
        # Check documentation
        print("\n📚 Checking Documentation:")
        self.check_file_exists("TESTING_GUIDE.md", "Testing guide")
        self.check_file_exists("TEST_QUICK_REFERENCE.md", "Quick reference")
        
        # Check directories
        print("\n📁 Checking Directories:")
        self.check_directory_exists("tests", "Tests directory")
        self.check_directory_exists("models", "Models directory")
        self.check_directory_exists("services", "Services directory")
        self.check_directory_exists("routes", "Routes directory")
        self.check_directory_exists("utils", "Utils directory")
        
        # Check pytest installation
        print("\n📦 Checking Dependencies:")
        self.check_pytest_installed()
        
        return len(self.issues) == 0

    def print_results(self):
        """Print verification results."""
        print("\n" + "=" * 60)
        print("📊 VERIFICATION RESULTS")
        print("=" * 60)
        
        print(f"\n✅ Successes: {len(self.successes)}")
        for success in self.successes:
            print(f"   {success}")
        
        if self.issues:
            print(f"\n❌ Issues: {len(self.issues)}")
            for issue in self.issues:
                print(f"   {issue}")
        else:
            print("\n✅ All checks passed! Setup is complete.")
        
        return len(self.issues) == 0

    def suggest_next_steps(self):
        """Suggest next steps."""
        print("\n" + "=" * 60)
        print("🚀 NEXT STEPS")
        print("=" * 60)
        print("""
1. Install dependencies (if not done):
   pip install -r requirements.txt

2. Run all tests:
   pytest -v

3. Run with coverage:
   pytest --cov=. --cov-report=html

4. View coverage report:
   htmlcov/index.html

5. Run specific tests:
   pytest -m unit           # Unit tests
   pytest -m integration    # Integration tests
   pytest -m edge_case      # Edge cases
   pytest -m negative       # Error handling

6. Review documentation:
   - TESTING_GUIDE.md
   - TEST_QUICK_REFERENCE.md
        """)


def main():
    """Main verification routine."""
    verifier = TestSetupVerifier()
    
    is_valid = verifier.verify_all()
    is_valid = verifier.print_results() and is_valid
    
    if is_valid:
        verifier.suggest_next_steps()
        print("\n✅ PYTEST SETUP IS COMPLETE AND VERIFIED!")
        print("=" * 60)
        return 0
    else:
        print("\n⚠️  Some issues found. Please resolve them and try again.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
