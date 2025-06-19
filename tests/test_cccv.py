#!/usr/bin/env python3
"""
CCCV1-CCCV4 Test Suite
=====================

Test script to verify CCCV1-CCCV4 functionality and reproducibility.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def test_cccv_structure():
    """Test CCCV1-CCCV4 directory structure"""
    
    print("Testing CCCV1-CCCV4 structure...")
    
    required_dirs = [
        'cccv1/src/models',
        'cccv1/scripts',
        'cccv2/src/models', 
        'cccv2/scripts',
        'cccv3/src/models',
        'cccv3/scripts',
        'cccv4/scripts'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"Missing CCCV directories: {missing_dirs}")
        return False
    
    print("All CCCV directories present")
    return True

def test_reproducibility_system():
    """Test reproducibility system"""
    
    print("Testing reproducibility system...")
    
    try:
        from enhanced_reproducibility import setup_full_reproducibility
        
        # Test basic setup
        manager = setup_full_reproducibility(seed=42, strict_mode=False, save_report=False)
        
        print("Reproducibility system working")
        return True
        
    except Exception as e:
        print(f"Reproducibility system error: {e}")
        return False

def test_data_loading():
    """Test data loading capability"""
    
    print("Testing data loading...")
    
    try:
        from src.data.loader import load_dataset_gpu_optimized
        
        print("Data loading system available")
        return True
        
    except Exception as e:
        print(f"Data loading error: {e}")
        return False

def test_training_script():
    """Test training script availability"""
    
    print("Testing training script...")
    
    if Path('train_cccv.py').exists():
        print("CCCV training script available")
        return True
    else:
        print("CCCV training script missing")
        return False

def test_documentation():
    """Test documentation availability"""
    
    print("Testing documentation...")
    
    required_docs = [
        'README.md',
        'REPRODUCIBILITY.md',
        'LICENSE',
        'requirements.txt'
    ]
    
    missing_docs = []
    for doc in required_docs:
        if not Path(doc).exists():
            missing_docs.append(doc)
    
    if missing_docs:
        print(f"Missing documentation: {missing_docs}")
        return False
    
    print("All documentation present")
    return True

def main():
    """Main test execution"""
    
    print("CCCV1-CCCV4 TEST SUITE")
    print("=" * 40)
    print("Testing CCCV1-CCCV4 release functionality...")
    
    tests = [
        ("CCCV Structure", test_cccv_structure),
        ("Reproducibility System", test_reproducibility_system),
        ("Data Loading", test_data_loading),
        ("Training Script", test_training_script),
        ("Documentation", test_documentation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        if test_func():
            passed += 1
        else:
            print(f"{test_name} FAILED")
    
    print("\n" + "=" * 40)
    print(f"CCCV1-CCCV4 TEST RESULTS: {passed}/{total} PASSED")
    
    if passed == total:
        print("ALL TESTS PASSED!")
        print("CCCV1-CCCV4 system ready")
    else:
        print("SOME TESTS FAILED!")
        print("Please check failed components")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
