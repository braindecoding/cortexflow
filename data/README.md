# CortexFlow CCCV1-CCCV4 Dataset Directory

## 📁 Dataset Structure

This directory contains the datasets used for training and evaluating CCCV1-CCCV4 models.

### 📊 **Supported Datasets**

#### **1. Miyawaki Dataset**
- **File**: `processed/miyawaki_structured_28x28.mat`
- **Description**: Visual cortex fMRI data
- **Samples**: 107 samples
- **Features**: 967 features
- **Target**: 28x28 grayscale images
- **Best CCCV**: CCCV4 (Meta-adaptive)

#### **2. Vangerven Dataset**
- **File**: `processed/vangerven_structured_28x28.mat`
- **Description**: Visual stimuli fMRI data
- **Samples**: 90 samples
- **Features**: 3092 features
- **Target**: 28x28 grayscale images
- **Best CCCV**: CCCV1 (Foundation)

#### **3. MindBigData Dataset**
- **File**: `processed/mindbigdata.mat`
- **Description**: Large-scale neural data
- **Samples**: 1080 samples
- **Features**: 3092 features
- **Target**: 28x28 grayscale images
- **Best CCCV**: CCCV3 (Ultimate)

#### **4. Crell Dataset**
- **File**: `processed/crell.mat`
- **Description**: Medium complexity dataset
- **Samples**: 576 samples
- **Features**: 3092 features
- **Target**: 28x28 grayscale images
- **Best CCCV**: CCCV3 (Ultimate)

### 📁 **Directory Structure**

```
data/
├── README.md              # This documentation
├── processed/             # Preprocessed datasets (*.mat files)
│   ├── miyawaki_structured_28x28.mat
│   ├── vangerven_structured_28x28.mat
│   ├── mindbigdata.mat
│   ├── crell.mat
│   └── digit69_28x28.mat
├── raw/                   # Raw dataset files
│   ├── S01.mat           # Raw Miyawaki data
│   └── EP1.01.txt        # Raw MindBigData
└── external/              # External dataset files
    ├── MindbigdataStimuli/
    └── crellStimuli/
```

### 🚨 **Important Notes**

#### **Dataset Files Not Included in Git**
Dataset files are **NOT included** in the git repository due to their large size:
- `processed/*.mat` files (1.6MB - 30MB each)
- `raw/*.mat` and `raw/*.txt` files (up to 2.7GB)
- `external/` directories with stimuli

#### **How to Obtain Datasets**
1. **Download from original sources**:
   - Miyawaki: [Original paper dataset]
   - Vangerven: [Original paper dataset]
   - MindBigData: [MindBigData website]
   - Crell: [Original paper dataset]

2. **Use data loading utilities**:
   ```python
   from src.data.loader import load_dataset_gpu_optimized
   
   # Load dataset (will download if not present)
   X_train, y_train, X_test, y_test = load_dataset_gpu_optimized('miyawaki')
   ```

3. **Manual placement**:
   - Place downloaded `.mat` files in `data/processed/`
   - Ensure filenames match the expected names above

### 🔧 **Data Loading**

#### **Automatic Loading**
```python
from src.data.loader import load_dataset_gpu_optimized

# Load any supported dataset
datasets = ['miyawaki', 'vangerven', 'mindbigdata', 'crell']
for dataset_name in datasets:
    X_train, y_train, X_test, y_test = load_dataset_gpu_optimized(dataset_name)
    print(f"{dataset_name}: {X_train.shape} -> {y_train.shape}")
```

#### **Manual Loading**
```python
import scipy.io as sio

# Load specific dataset
data = sio.loadmat('data/processed/miyawaki_structured_28x28.mat')
X = data['X']  # fMRI features
y = data['y']  # Target images
```

### 📊 **Dataset Characteristics**

| Dataset | Samples | Features | Complexity | Best CCCV |
|---------|---------|----------|------------|-----------|
| **Miyawaki** | 107 | 967 | High | CCCV4 |
| **Vangerven** | 90 | 3092 | Medium | CCCV1 |
| **MindBigData** | 1080 | 3092 | Large | CCCV3 |
| **Crell** | 576 | 3092 | Medium | CCCV3 |

### ✅ **Reproducibility**

All datasets are loaded with:
- **Consistent preprocessing**: Same normalization and structure
- **Reproducible splits**: Fixed random seeds for train/test splits
- **Cross-validation**: 10-fold CV with consistent fold generation
- **GPU optimization**: Efficient loading for CUDA devices

### 🎯 **Usage in CCCV Models**

Each CCCV model automatically handles dataset loading:
```python
# CCCV4 automatically selects optimal strategy per dataset
from cccv4.scripts.test_cccv4_simplified import CCCV4ProxyModel

model = CCCV4ProxyModel(input_dim, dataset_name, dataset_size, device)
reconstructions, meta_info = model(X_fmri)
```

---

**📝 Note**: Dataset files are excluded from git due to size constraints. Please download datasets separately and place them in the appropriate directories.
