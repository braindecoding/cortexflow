"""
Enhanced Reproducibility System for CortexFlow CCCV1-CCCV4
=========================================================

Advanced reproducibility utilities for scientific research integrity.

Features:
- Multi-level seed management
- Environment reproducibility
- Hardware-specific optimizations
- Statistical validation
- Reproducibility verification

Usage:
    from enhanced_reproducibility import setup_full_reproducibility
    setup_full_reproducibility(seed=42, strict_mode=True)
"""

import torch
import numpy as np
import random
import os
import sys
import platform
import hashlib
from datetime import datetime
from pathlib import Path

class ReproducibilityManager:
    """Advanced reproducibility management system"""
    
    def __init__(self, seed=42, strict_mode=True):
        self.seed = seed
        self.strict_mode = strict_mode
        self.environment_info = {}
        self.setup_info = {}
        
    def setup_full_reproducibility(self):
        """Setup comprehensive reproducibility"""
        
        print("🔧 SETTING UP ENHANCED REPRODUCIBILITY")
        print("=" * 50)
        
        # 1. Basic seed setting
        self._set_basic_seeds()
        
        # 2. Advanced PyTorch settings
        self._set_pytorch_deterministic()
        
        # 3. Environment variables
        self._set_environment_variables()
        
        # 4. Hardware-specific settings
        self._set_hardware_specific()
        
        # 5. Record environment
        self._record_environment()
        
        # 6. Verification
        if self.strict_mode:
            self._verify_reproducibility()
        
        print("✅ Enhanced reproducibility setup completed!")
        return self.setup_info
    
    def _set_basic_seeds(self):
        """Set basic random seeds"""
        torch.manual_seed(self.seed)
        torch.cuda.manual_seed(self.seed)
        torch.cuda.manual_seed_all(self.seed)
        np.random.seed(self.seed)
        random.seed(self.seed)
        
        self.setup_info['basic_seeds'] = True
        print(f"✅ Basic seeds set to {self.seed}")
    
    def _set_pytorch_deterministic(self):
        """Set PyTorch deterministic operations"""
        
        # Deterministic operations
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        
        # Additional deterministic settings
        torch.use_deterministic_algorithms(True, warn_only=True)
        
        # Set number of threads for reproducibility
        torch.set_num_threads(1)
        
        self.setup_info['pytorch_deterministic'] = True
        print("✅ PyTorch deterministic operations enabled")
    
    def _set_environment_variables(self):
        """Set environment variables for reproducibility"""
        
        # CUDA settings
        os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
        os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
        
        # Python hash seed
        os.environ['PYTHONHASHSEED'] = str(self.seed)
        
        # OpenMP settings
        os.environ['OMP_NUM_THREADS'] = '1'
        os.environ['MKL_NUM_THREADS'] = '1'
        
        self.setup_info['environment_variables'] = True
        print("✅ Environment variables set for reproducibility")
    
    def _set_hardware_specific(self):
        """Set hardware-specific reproducibility settings"""
        
        if torch.cuda.is_available():
            # GPU-specific settings
            torch.cuda.empty_cache()
            
            # Set GPU deterministic operations
            for i in range(torch.cuda.device_count()):
                with torch.cuda.device(i):
                    torch.cuda.manual_seed(self.seed)
            
            self.setup_info['gpu_settings'] = True
            print(f"✅ GPU reproducibility set for {torch.cuda.device_count()} devices")
        else:
            self.setup_info['gpu_settings'] = False
            print("✅ CPU-only reproducibility settings applied")
    
    def _record_environment(self):
        """Record environment information for reproducibility"""
        
        self.environment_info = {
            'timestamp': datetime.now().isoformat(),
            'seed': self.seed,
            'python_version': sys.version,
            'platform': platform.platform(),
            'torch_version': torch.__version__,
            'numpy_version': np.__version__,
            'cuda_available': torch.cuda.is_available(),
            'cuda_version': torch.version.cuda if torch.cuda.is_available() else None,
            'gpu_count': torch.cuda.device_count() if torch.cuda.is_available() else 0,
            'gpu_names': [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())] if torch.cuda.is_available() else [],
            'strict_mode': self.strict_mode
        }
        
        print("✅ Environment information recorded")
    
    def _verify_reproducibility(self):
        """Verify reproducibility setup"""
        
        print("🔍 Verifying reproducibility setup...")
        
        # Test basic reproducibility
        torch.manual_seed(self.seed)
        test_tensor1 = torch.randn(10, 10)
        
        torch.manual_seed(self.seed)
        test_tensor2 = torch.randn(10, 10)
        
        if torch.allclose(test_tensor1, test_tensor2):
            print("✅ Basic reproducibility verified")
            self.setup_info['verification_passed'] = True
        else:
            print("❌ Basic reproducibility verification failed")
            self.setup_info['verification_passed'] = False
    
    def save_reproducibility_report(self, output_dir="results"):
        """Save reproducibility report"""
        
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = output_dir / f"reproducibility_report_{timestamp}.json"
        
        import json
        report_data = {
            'setup_info': self.setup_info,
            'environment_info': self.environment_info
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"📝 Reproducibility report saved: {report_file}")
        return report_file

def setup_full_reproducibility(seed=42, strict_mode=True, save_report=True):
    """
    Setup comprehensive reproducibility for CortexFlow experiments
    
    Args:
        seed: Random seed value
        strict_mode: Enable strict reproducibility checks
        save_report: Save reproducibility report
    
    Returns:
        ReproducibilityManager instance
    """
    
    manager = ReproducibilityManager(seed=seed, strict_mode=strict_mode)
    setup_info = manager.setup_full_reproducibility()
    
    if save_report:
        manager.save_reproducibility_report()
    
    return manager

def create_reproducible_cross_validation(n_splits=5, n_runs=3, base_seed=42):
    """
    Create reproducible cross-validation setup
    
    Args:
        n_splits: Number of CV folds
        n_runs: Number of independent runs
        base_seed: Base seed for reproducibility
    
    Returns:
        List of (KFold, seed) tuples for each run
    """
    from sklearn.model_selection import KFold
    
    cv_setups = []
    
    for run in range(n_runs):
        run_seed = base_seed + run
        kfold = KFold(n_splits=n_splits, shuffle=True, random_state=run_seed)
        cv_setups.append((kfold, run_seed))
    
    print(f"✅ Created {n_runs} reproducible CV setups with {n_splits} folds each")
    return cv_setups

def verify_dataset_reproducibility(dataset_loader_func, dataset_name, n_checks=3):
    """
    Verify that dataset loading is reproducible
    
    Args:
        dataset_loader_func: Function to load dataset
        dataset_name: Name of dataset
        n_checks: Number of loading checks
    
    Returns:
        bool: True if reproducible, False otherwise
    """
    
    print(f"🔍 Verifying dataset reproducibility: {dataset_name}")
    
    checksums = []
    
    for i in range(n_checks):
        # Reset seeds
        torch.manual_seed(42)
        np.random.seed(42)
        
        # Load dataset
        try:
            X_train, y_train, X_test, y_test, input_dim = dataset_loader_func(dataset_name, 'cpu')
            
            # Create checksum
            data_str = f"{X_train.sum().item()}{y_train.sum().item()}{X_test.sum().item()}{y_test.sum().item()}"
            checksum = hashlib.md5(data_str.encode()).hexdigest()
            checksums.append(checksum)
            
        except Exception as e:
            print(f"❌ Dataset loading failed: {e}")
            return False
    
    # Check if all checksums are identical
    if len(set(checksums)) == 1:
        print(f"✅ Dataset loading is reproducible: {dataset_name}")
        return True
    else:
        print(f"❌ Dataset loading is NOT reproducible: {dataset_name}")
        return False

def main():
    """Test enhanced reproducibility system"""
    
    print("🧪 TESTING ENHANCED REPRODUCIBILITY SYSTEM")
    print("=" * 60)
    
    # Setup full reproducibility
    manager = setup_full_reproducibility(seed=42, strict_mode=True)
    
    # Test cross-validation setup
    cv_setups = create_reproducible_cross_validation(n_splits=5, n_runs=3)
    
    print(f"\n📊 REPRODUCIBILITY SUMMARY:")
    print(f"✅ Seed: {manager.seed}")
    print(f"✅ Strict mode: {manager.strict_mode}")
    print(f"✅ Verification: {manager.setup_info.get('verification_passed', False)}")
    print(f"✅ GPU settings: {manager.setup_info.get('gpu_settings', False)}")
    print(f"✅ CV setups: {len(cv_setups)} runs with 5 folds each")
    
    print(f"\n🎯 ENHANCED REPRODUCIBILITY SYSTEM READY!")

if __name__ == "__main__":
    main()
