"""
Dataset Loading and Preprocessing (ACADEMIC INTEGRITY COMPLIANT)
===============================================================

GPU-optimized dataset loading functions for neural decoding research.
FIXED: Eliminates data leakage by using training statistics for test normalization.

Supported Datasets:
    - Miyawaki: Visual complex patterns (28x28 binary contrast)
    - Vangerven: Digit patterns (28x28 grayscale)
    - MindBigData: EEG→fMRI→Visual translation
    - Crell: EEG→fMRI→Visual translation

Features:
    - GPU-optimized loading and preprocessing
    - ACADEMIC INTEGRITY: No data leakage in preprocessing
    - Training statistics used for test set normalization
    - Cross-validation compatible preprocessing
    - WSL-compatible configuration
    - Memory-efficient processing

CRITICAL FIX: This version eliminates the data leakage issue where test set
statistics were used for test set normalization. Now uses training statistics
for both training and test set normalization.
"""

import torch
import scipy.io as sio
from pathlib import Path


def load_dataset_gpu_optimized(dataset_name, device='cuda'):
    """
    Load dataset dengan GPU optimization (ACADEMIC INTEGRITY COMPLIANT)

    Loads neural decoding datasets directly to GPU memory with proper
    preprocessing that eliminates data leakage.

    CRITICAL FIX: Uses training statistics for test set normalization
    to prevent data leakage and ensure academic integrity.

    Args:
        dataset_name: Name of dataset ('miyawaki', 'vangerven', 'mindbigdata', 'crell')
        device: Target device for tensor loading ('cuda' or 'cpu')

    Returns:
        tuple: (X_train, y_train, X_test, y_test, input_dim)
            - X_train: Training fMRI signals [N, input_dim] (normalized with train stats)
            - y_train: Training visual stimuli [N, 1, 28, 28]
            - X_test: Test fMRI signals [M, input_dim] (normalized with train stats)
            - y_test: Test visual stimuli [M, 1, 28, 28]
            - input_dim: Dimensionality of fMRI signals

    Academic Integrity:
        - Training statistics (mean, std) computed from training set only
        - Same statistics applied to both training and test sets
        - Eliminates data leakage from test set statistics
    """
    
    print(f"🚀 Loading {dataset_name} dataset untuk GPU training...")
    
    data_path = Path("data/processed")
    
    dataset_files = {
        'miyawaki': 'miyawaki_structured_28x28.mat',
        'vangerven': 'digit69_28x28.mat',
        'mindbigdata': 'mindbigdata.mat',
        'crell': 'crell.mat'
    }
    
    if dataset_name not in dataset_files:
        print(f"❌ Dataset {dataset_name} not supported")
        print(f"   Supported datasets: {list(dataset_files.keys())}")
        return None, None, None, None, 0
    
    mat_file = data_path / dataset_files[dataset_name]
    
    if not mat_file.exists():
        print(f"❌ Dataset file not found: {mat_file}")
        print(f"   Please ensure the dataset is in the data/processed/ directory")
        return None, None, None, None, 0
    
    try:
        data = sio.loadmat(str(mat_file))
    except Exception as e:
        print(f"❌ Error loading dataset file: {e}")
        return None, None, None, None, 0
    
    # Load ke GPU langsung untuk memory efficiency
    try:
        X_train = torch.tensor(data['fmriTrn'], dtype=torch.float32, device=device)
        y_train = torch.tensor(data['stimTrn'], dtype=torch.float32, device=device)
        X_test = torch.tensor(data['fmriTest'], dtype=torch.float32, device=device)
        y_test = torch.tensor(data['stimTest'], dtype=torch.float32, device=device)
    except KeyError as e:
        print(f"❌ Missing required data field in dataset: {e}")
        print(f"   Expected fields: fmriTrn, stimTrn, fmriTest, stimTest")
        return None, None, None, None, 0
    except Exception as e:
        print(f"❌ Error converting data to tensors: {e}")
        return None, None, None, None, 0
    
    # ACADEMIC INTEGRITY FIX: Use training statistics for both sets
    # Compute normalization statistics from training set ONLY
    train_mean = X_train.mean()
    train_std = X_train.std()

    # Apply training statistics to both training and test sets
    X_train = (X_train - train_mean) / (train_std + 1e-8)
    X_test = (X_test - train_mean) / (train_std + 1e-8)

    print(f"🔒 ACADEMIC INTEGRITY: Using training statistics for normalization")
    print(f"   Training mean: {train_mean:.6f}, std: {train_std:.6f}")
    print(f"   Applied to both training and test sets")
    
    # Dataset-specific preprocessing
    if dataset_name == 'miyawaki':
        # Miyawaki: Binary contrast images (black/white patterns)
        y_train = y_train.view(-1, 1, 28, 28)
        y_test = y_test.view(-1, 1, 28, 28)
        y_train = (y_train - y_train.min()) / (y_train.max() - y_train.min() + 1e-8)
        y_test = (y_test - y_test.min()) / (y_test.max() - y_test.min() + 1e-8)
        
    elif dataset_name == 'vangerven':
        # Vangerven: Digit patterns (0-255 grayscale)
        y_train = y_train.view(-1, 1, 28, 28) / 255.0
        y_test = y_test.view(-1, 1, 28, 28) / 255.0
        
    else:  # mindbigdata, crell
        # EEG→fMRI→Visual datasets
        y_train = y_train.view(-1, 1, 28, 28)
        y_test = y_test.view(-1, 1, 28, 28)
        y_train = (y_train - y_train.min()) / (y_train.max() - y_train.min() + 1e-8)
        y_test = (y_test - y_test.min()) / (y_test.max() - y_test.min() + 1e-8)
    
    input_dim = X_train.shape[1]
    
    print(f"✅ Dataset loaded ke GPU: X_train={X_train.shape}, y_train={y_train.shape}")
    print(f"   Input dimension: {input_dim}")
    print(f"   Device: {device}")
    print(f"   Memory usage optimized for {dataset_name} dataset")
    
    return X_train, y_train, X_test, y_test, input_dim


def load_dataset_raw(dataset_name, device='cuda'):
    """
    Load dataset WITHOUT preprocessing for cross-validation use.

    This function loads raw data without normalization, allowing proper
    preprocessing within each CV fold to prevent data leakage.

    Args:
        dataset_name: Name of dataset ('miyawaki', 'vangerven', 'mindbigdata', 'crell')
        device: Target device for tensor loading ('cuda' or 'cpu')

    Returns:
        tuple: (X_train_raw, y_train_raw, X_test_raw, y_test_raw, input_dim, preprocess_fn)
            - X_train_raw: Raw training fMRI signals [N, input_dim] (NOT normalized)
            - y_train_raw: Raw training visual stimuli [N, H, W] (NOT normalized)
            - X_test_raw: Raw test fMRI signals [M, input_dim] (NOT normalized)
            - y_test_raw: Raw test visual stimuli [M, H, W] (NOT normalized)
            - input_dim: Dimensionality of fMRI signals
            - preprocess_fn: Function to apply preprocessing with given statistics
    """

    print(f"🚀 Loading {dataset_name} dataset (RAW - for CV use)...")

    data_path = Path("data/processed")

    dataset_files = {
        'miyawaki': 'miyawaki_structured_28x28.mat',
        'vangerven': 'digit69_28x28.mat',
        'mindbigdata': 'mindbigdata.mat',
        'crell': 'crell.mat'
    }

    if dataset_name not in dataset_files:
        print(f"❌ Dataset {dataset_name} not supported")
        print(f"   Supported datasets: {list(dataset_files.keys())}")
        return None, None, None, None, 0, None

    mat_file = data_path / dataset_files[dataset_name]

    if not mat_file.exists():
        print(f"❌ Dataset file not found: {mat_file}")
        print(f"   Please ensure the dataset is in the data/processed/ directory")
        return None, None, None, None, 0, None

    try:
        data = sio.loadmat(str(mat_file))
    except Exception as e:
        print(f"❌ Error loading dataset file: {e}")
        return None, None, None, None, 0, None

    # Load ke GPU langsung untuk memory efficiency (RAW - no preprocessing)
    try:
        X_train_raw = torch.tensor(data['fmriTrn'], dtype=torch.float32, device=device)
        y_train_raw = torch.tensor(data['stimTrn'], dtype=torch.float32, device=device)
        X_test_raw = torch.tensor(data['fmriTest'], dtype=torch.float32, device=device)
        y_test_raw = torch.tensor(data['stimTest'], dtype=torch.float32, device=device)
    except KeyError as e:
        print(f"❌ Missing required data field in dataset: {e}")
        print(f"   Expected fields: fmriTrn, stimTrn, fmriTest, stimTest")
        return None, None, None, None, 0, None
    except Exception as e:
        print(f"❌ Error converting data to tensors: {e}")
        return None, None, None, None, 0, None

    input_dim = X_train_raw.shape[1]

    # Create preprocessing function for this dataset
    def preprocess_fn(X_train_fold, y_train_fold, X_val_fold, y_val_fold):
        """
        Apply preprocessing using training fold statistics only.

        Args:
            X_train_fold: Training fold fMRI data
            y_train_fold: Training fold visual data
            X_val_fold: Validation fold fMRI data
            y_val_fold: Validation fold visual data

        Returns:
            Preprocessed data with training fold statistics
        """
        # Compute statistics from training fold ONLY
        train_mean = X_train_fold.mean()
        train_std = X_train_fold.std()

        # Apply to both training and validation folds
        X_train_processed = (X_train_fold - train_mean) / (train_std + 1e-8)
        X_val_processed = (X_val_fold - train_mean) / (train_std + 1e-8)

        # Dataset-specific y preprocessing
        if dataset_name == 'miyawaki':
            # Miyawaki: Binary contrast images
            y_train_processed = y_train_fold.view(-1, 1, 28, 28)
            y_val_processed = y_val_fold.view(-1, 1, 28, 28)
            y_train_processed = (y_train_processed - y_train_processed.min()) / (y_train_processed.max() - y_train_processed.min() + 1e-8)
            y_val_processed = (y_val_processed - y_val_processed.min()) / (y_val_processed.max() - y_val_processed.min() + 1e-8)

        elif dataset_name == 'vangerven':
            # Vangerven: Digit patterns
            y_train_processed = y_train_fold.view(-1, 1, 28, 28) / 255.0
            y_val_processed = y_val_fold.view(-1, 1, 28, 28) / 255.0

        else:  # mindbigdata, crell
            # EEG→fMRI→Visual datasets
            y_train_processed = y_train_fold.view(-1, 1, 28, 28)
            y_val_processed = y_val_fold.view(-1, 1, 28, 28)
            y_train_processed = (y_train_processed - y_train_processed.min()) / (y_train_processed.max() - y_train_processed.min() + 1e-8)
            y_val_processed = (y_val_processed - y_val_processed.min()) / (y_val_processed.max() - y_val_processed.min() + 1e-8)

        return X_train_processed, y_train_processed, X_val_processed, y_val_processed

    print(f"✅ Raw dataset loaded ke GPU: X_train={X_train_raw.shape}, y_train={y_train_raw.shape}")
    print(f"   Input dimension: {input_dim}")
    print(f"   Device: {device}")
    print(f"   🔒 ACADEMIC INTEGRITY: Raw data for proper CV preprocessing")

    return X_train_raw, y_train_raw, X_test_raw, y_test_raw, input_dim, preprocess_fn


def get_dataset_info(dataset_name):
    """
    Get information about a specific dataset.
    
    Args:
        dataset_name: Name of the dataset
        
    Returns:
        Dictionary with dataset information
    """
    
    dataset_info = {
        'miyawaki': {
            'description': 'Visual complex patterns (binary contrast)',
            'image_type': 'Binary contrast (black/white)',
            'complexity': 'High (complex visual patterns)',
            'source': 'Miyawaki et al. fMRI visual reconstruction',
            'preprocessing': 'Min-max normalization',
            'characteristics': 'Lego-like block patterns, geometric shapes'
        },
        'vangerven': {
            'description': 'Digit patterns (grayscale)',
            'image_type': 'Grayscale digits (0-9)',
            'complexity': 'Medium (digit recognition)',
            'source': 'Vangerven et al. digit reconstruction',
            'preprocessing': 'Division by 255.0',
            'characteristics': 'Handwritten digit patterns'
        },
        'mindbigdata': {
            'description': 'EEG→fMRI→Visual translation',
            'image_type': 'Translated visual patterns',
            'complexity': 'High (cross-modal translation)',
            'source': 'MindBigData EEG-to-visual dataset',
            'preprocessing': 'Min-max normalization',
            'characteristics': 'EEG signals translated to fMRI then to visual'
        },
        'crell': {
            'description': 'EEG→fMRI→Visual translation',
            'image_type': 'Translated visual patterns',
            'complexity': 'High (cross-modal translation)',
            'source': 'Crell EEG-to-visual dataset',
            'preprocessing': 'Min-max normalization',
            'characteristics': 'EEG signals translated to fMRI then to visual'
        }
    }
    
    return dataset_info.get(dataset_name, {
        'description': 'Unknown dataset',
        'image_type': 'Unknown',
        'complexity': 'Unknown',
        'source': 'Unknown',
        'preprocessing': 'Unknown',
        'characteristics': 'Unknown'
    })


def validate_dataset_structure(dataset_name):
    """
    Validate that a dataset has the correct structure.
    
    Args:
        dataset_name: Name of the dataset to validate
        
    Returns:
        bool: True if dataset structure is valid, False otherwise
    """
    
    data_path = Path("data/processed")
    dataset_files = {
        'miyawaki': 'miyawaki_structured_28x28.mat',
        'vangerven': 'digit69_28x28.mat',
        'mindbigdata': 'mindbigdata.mat',
        'crell': 'crell.mat'
    }
    
    if dataset_name not in dataset_files:
        print(f"❌ Unknown dataset: {dataset_name}")
        return False
    
    mat_file = data_path / dataset_files[dataset_name]
    
    if not mat_file.exists():
        print(f"❌ Dataset file not found: {mat_file}")
        return False
    
    try:
        data = sio.loadmat(str(mat_file))
        required_fields = ['fmriTrn', 'stimTrn', 'fmriTest', 'stimTest']
        
        for field in required_fields:
            if field not in data:
                print(f"❌ Missing required field: {field}")
                return False
        
        print(f"✅ Dataset {dataset_name} structure is valid")
        print(f"   fmriTrn: {data['fmriTrn'].shape}")
        print(f"   stimTrn: {data['stimTrn'].shape}")
        print(f"   fmriTest: {data['fmriTest'].shape}")
        print(f"   stimTest: {data['stimTest'].shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating dataset: {e}")
        return False


def list_available_datasets():
    """
    List all available datasets in the data/processed directory.
    
    Returns:
        List of available dataset names
    """
    
    data_path = Path("data/processed")
    dataset_files = {
        'miyawaki': 'miyawaki_structured_28x28.mat',
        'vangerven': 'digit69_28x28.mat',
        'mindbigdata': 'mindbigdata.mat',
        'crell': 'crell.mat'
    }
    
    available_datasets = []
    
    print("📊 CHECKING AVAILABLE DATASETS:")
    print("=" * 40)
    
    for dataset_name, filename in dataset_files.items():
        mat_file = data_path / filename
        if mat_file.exists():
            available_datasets.append(dataset_name)
            print(f"✅ {dataset_name}: {filename}")
        else:
            print(f"❌ {dataset_name}: {filename} (not found)")
    
    print(f"\n📈 Available datasets: {len(available_datasets)}/{len(dataset_files)}")
    
    return available_datasets


if __name__ == "__main__":
    # Test dataset loading
    print("🧪 TESTING DATASET LOADING")
    print("=" * 40)
    
    available = list_available_datasets()
    
    if available:
        test_dataset = available[0]
        print(f"\n🔧 Testing dataset: {test_dataset}")
        
        # Test validation
        is_valid = validate_dataset_structure(test_dataset)
        
        if is_valid:
            # Test loading
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            X_train, y_train, X_test, y_test, input_dim = load_dataset_gpu_optimized(test_dataset, device)
            
            if X_train is not None:
                print(f"✅ Dataset loading test successful!")
                print(f"   Device: {device}")
                print(f"   Input dimension: {input_dim}")
            else:
                print(f"❌ Dataset loading test failed")
        else:
            print(f"❌ Dataset validation failed")
    else:
        print("❌ No datasets available for testing")
