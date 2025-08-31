#!/usr/bin/env python3

"""
Monopogen-Fixed Setup Verification Script
Checks if all dependencies and tools are properly installed and configured.
"""

import os
import sys
import subprocess
import importlib
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def check_python_packages():
    """Check if required Python packages are installed."""
    logger.info("Checking Python packages...")
    
    required_packages = [
        'numpy', 'scipy', 'pandas', 'pysam', 'cyvcf2', 
        'sklearn', 'matplotlib', 'seaborn', 'tqdm'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                importlib.import_module('sklearn')
            else:
                importlib.import_module(package)
            logger.info(f"✅ {package} - OK")
        except ImportError:
            logger.error(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    return missing_packages

def check_external_tools():
    """Check if external bioinformatics tools are available."""
    logger.info("Checking external tools...")
    
    tools = {
        'samtools': 'samtools --version',
        'bcftools': 'bcftools --version',
        'tabix': 'tabix --version',
        'bgzip': 'bgzip --version'
    }
    
    missing_tools = []
    
    for tool, cmd in tools.items():
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version = result.stdout.split('\n')[0] if result.stdout else "Unknown version"
                logger.info(f"✅ {tool} - {version}")
            else:
                logger.error(f"❌ {tool} - Command failed")
                missing_tools.append(tool)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.error(f"❌ {tool} - NOT FOUND")
            missing_tools.append(tool)
    
    return missing_tools

def check_file_structure():
    """Check if the repository has the expected file structure."""
    logger.info("Checking file structure...")
    
    expected_files = [
        'src/main.py',
        'src/bamProcess.py',
        'scripts/fix_vcf_headers.sh',
        'requirements.txt',
        'config/config_template.ini'
    ]
    
    missing_files = []
    
    for file_path in expected_files:
        if os.path.exists(file_path):
            logger.info(f"✅ {file_path} - EXISTS")
        else:
            logger.error(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    return missing_files

def check_permissions():
    """Check if scripts have executable permissions."""
    logger.info("Checking script permissions...")
    
    scripts = [
        'scripts/fix_vcf_headers.sh'
    ]
    
    permission_issues = []
    
    for script in scripts:
        if os.path.exists(script):
            if os.access(script, os.X_OK):
                logger.info(f"✅ {script} - EXECUTABLE")
            else:
                logger.warning(f"⚠️  {script} - NOT EXECUTABLE (run: chmod +x {script})")
                permission_issues.append(script)
        else:
            logger.error(f"❌ {script} - FILE NOT FOUND")
            permission_issues.append(script)
    
    return permission_issues

def main():
    """Main verification function."""
    print("=" * 60)
    print("    Monopogen-Fixed Setup Verification")
    print("=" * 60)
    print()
    
    # Check Python packages
    missing_packages = check_python_packages()
    print()
    
    # Check external tools
    missing_tools = check_external_tools()
    print()
    
    # Check file structure
    missing_files = check_file_structure()
    print()
    
    # Check permissions
    permission_issues = check_permissions()
    print()
    
    # Summary
    print("=" * 60)
    print("    VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_good = True
    
    if missing_packages:
        print(f"❌ Missing Python packages: {', '.join(missing_packages)}")
        print(f"   Fix: pip install -r requirements.txt")
        all_good = False
    else:
        print("✅ All Python packages are installed")
    
    if missing_tools:
        print(f"❌ Missing external tools: {', '.join(missing_tools)}")
        print(f"   Fix: Install missing tools or update PATH")
        all_good = False
    else:
        print("✅ All external tools are available")
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        print(f"   Fix: Create missing files or check repository structure")
        all_good = False
    else:
        print("✅ All required files are present")
    
    if permission_issues:
        print(f"⚠️  Permission issues: {', '.join(permission_issues)}")
        print(f"   Fix: chmod +x scripts/*.sh")
        all_good = False
    else:
        print("✅ All scripts have proper permissions")
    
    print()
    
    if all_good:
        print("🎉 SETUP VERIFICATION PASSED!")
        print("   Your Monopogen-Fixed installation is ready to use.")
        return 0
    else:
        print("⚠️  SETUP VERIFICATION FAILED!")
        print("   Please fix the issues above before running the pipeline.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
