#!/usr/bin/env python3
"""
AEGIS-X System Verification Script
Comprehensive verification of all system components and workflow compatibility
"""

import os
import sys
import subprocess
import json
import yaml
from pathlib import Path
import importlib.util
import tempfile
import shutil

def print_header(title):
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def verify_workflow_syntax():
    """Verify GitHub Actions workflow syntax"""
    print_header("WORKFLOW SYNTAX VERIFICATION")
    
    workflow_file = Path(".github/workflows/ultimate_hunt.yml")
    if not workflow_file.exists():
        print_error("Workflow file not found")
        return False
    
    try:
        with open(workflow_file) as f:
            workflow_data = yaml.safe_load(f)
        print_success("Workflow YAML syntax is valid")
        
        # Check for required sections (note: 'on' becomes True in YAML)
        required_sections = ['name', True, 'jobs']  # 'on' becomes True in YAML
        section_names = ['name', 'on', 'jobs']
        for section, section_name in zip(required_sections, section_names):
            if section in workflow_data:
                print_success(f"Required section '{section_name}' found")
            else:
                print_error(f"Required section '{section_name}' missing")
                print_error(f"Available sections: {list(workflow_data.keys())}")
                return False
        
        # Check for updated actions
        workflow_content = workflow_file.read_text()
        if "actions/upload-artifact@v4" in workflow_content:
            print_success("Using updated upload-artifact@v4")
        else:
            print_error("Still using deprecated upload-artifact version")
            return False
            
        return True
        
    except yaml.YAMLError as e:
        print_error(f"Workflow YAML syntax error: {e}")
        return False

def verify_python_scripts():
    """Verify Python scripts compile correctly"""
    print_header("PYTHON SCRIPTS VERIFICATION")
    
    scripts_to_check = [
        "aegis_x_ultimate_master.py",
        "core/headless_evidence_collector.py",
        "core/advanced_professional_hunter.py",
        "core/advanced_verification_engine.py"
    ]
    
    all_valid = True
    for script in scripts_to_check:
        script_path = Path(script)
        if not script_path.exists():
            print_warning(f"Script {script} not found")
            continue
            
        try:
            # Compile the script
            subprocess.run([sys.executable, "-m", "py_compile", script], 
                         check=True, capture_output=True)
            print_success(f"Script {script} compiles successfully")
        except subprocess.CalledProcessError as e:
            print_error(f"Script {script} compilation failed: {e}")
            all_valid = False
    
    return all_valid

def verify_directory_structure():
    """Verify required directory structure"""
    print_header("DIRECTORY STRUCTURE VERIFICATION")
    
    required_dirs = [
        "core",
        "agents", 
        "hunters",
        "tools",
        "wordlists",
        ".github/workflows"
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print_success(f"Directory {dir_name} exists")
        else:
            print_error(f"Directory {dir_name} missing")
            all_exist = False
    
    return all_exist

def verify_evidence_collector():
    """Verify evidence collector functionality"""
    print_header("EVIDENCE COLLECTOR VERIFICATION")
    
    try:
        # Import the evidence collector
        from core.headless_evidence_collector import HeadlessEvidenceCollector
        
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_evidence_dir = Path(temp_dir) / "evidence"
            
            # Initialize evidence collector
            collector = HeadlessEvidenceCollector(temp_evidence_dir)
            print_success("Evidence collector initialized successfully")
            
            # Check if directories were created
            expected_dirs = ["screenshots", "videos", "network", "logs", "payloads", "reports"]
            for dir_name in expected_dirs:
                dir_path = temp_evidence_dir / dir_name
                if dir_path.exists():
                    print_success(f"Evidence directory {dir_name} created")
                    
                    # Check for initialization file
                    init_file = dir_path / ".evidence_collector_initialized"
                    if init_file.exists():
                        print_success(f"Initialization file created in {dir_name}")
                    else:
                        print_error(f"Initialization file missing in {dir_name}")
                        return False
                else:
                    print_error(f"Evidence directory {dir_name} not created")
                    return False
        
        return True
        
    except Exception as e:
        print_error(f"Evidence collector verification failed: {e}")
        return False

def verify_requirements():
    """Verify requirements files"""
    print_header("REQUIREMENTS VERIFICATION")
    
    req_files = ["requirements.txt", "requirements_core.txt"]
    all_valid = True
    
    for req_file in req_files:
        req_path = Path(req_file)
        if req_path.exists():
            print_success(f"Requirements file {req_file} exists")
            
            # Check for common issues
            content = req_path.read_text()
            if "==" in content or ">=" in content:
                print_success(f"Requirements file {req_file} has version specifications")
            else:
                print_warning(f"Requirements file {req_file} lacks version specifications")
        else:
            print_error(f"Requirements file {req_file} missing")
            all_valid = False
    
    return all_valid

def simulate_workflow_directories():
    """Simulate workflow directory creation"""
    print_header("WORKFLOW DIRECTORY SIMULATION")
    
    try:
        # Create temporary directories as workflow would
        temp_dirs = [
            "output/reports",
            "output/campaigns", 
            "evidence/screenshots",
            "evidence/videos",
            "evidence/network",
            "evidence/logs",
            "evidence/payloads",
            "evidence/reports",
            "logs"
        ]
        
        for dir_path in temp_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            
            # Create placeholder file as workflow would
            placeholder = Path(dir_path) / ".hunt_started"
            placeholder.write_text(f"Hunt started simulation\nDirectory: {dir_path}\n")
            
            print_success(f"Created directory {dir_path} with placeholder")
        
        # Verify all directories have files
        for dir_path in temp_dirs:
            files = list(Path(dir_path).glob("*"))
            if files:
                print_success(f"Directory {dir_path} contains {len(files)} files")
            else:
                print_error(f"Directory {dir_path} is empty")
                return False
        
        # Cleanup
        for root_dir in ["output", "evidence", "logs"]:
            if Path(root_dir).exists():
                shutil.rmtree(root_dir)
        
        return True
        
    except Exception as e:
        print_error(f"Directory simulation failed: {e}")
        return False

def main():
    """Run comprehensive system verification"""
    print("🔥" * 60)
    print("🚀 AEGIS-X SYSTEM VERIFICATION")
    print("🔥" * 60)
    
    verifications = [
        ("Workflow Syntax", verify_workflow_syntax),
        ("Python Scripts", verify_python_scripts),
        ("Directory Structure", verify_directory_structure),
        ("Evidence Collector", verify_evidence_collector),
        ("Requirements Files", verify_requirements),
        ("Workflow Directories", simulate_workflow_directories)
    ]
    
    results = {}
    for name, verify_func in verifications:
        try:
            results[name] = verify_func()
        except Exception as e:
            print_error(f"Verification {name} failed with exception: {e}")
            results[name] = False
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for name, result in results.items():
        if result:
            print_success(f"{name}: PASSED")
        else:
            print_error(f"{name}: FAILED")
    
    print(f"\n📊 Overall Result: {passed}/{total} verifications passed")
    
    if passed == total:
        print_success("🎉 ALL VERIFICATIONS PASSED! System is ready.")
        return 0
    else:
        print_error(f"❌ {total - passed} verifications failed. System needs fixes.")
        return 1

if __name__ == "__main__":
    sys.exit(main())