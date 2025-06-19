# CCCV3 Model Templates

## 📁 Pre-trained Model Templates

This directory contains pre-trained model templates for CCCV3 transfer learning.

### 🎯 **Template Models**

#### **1. Attention Templates**
- `attention_miyawaki_template.pth` (12.46 MB)
- `attention_mindbigdata_template.pth` (28.65 MB)  
- `attention_crell_template.pth` (28.65 MB)

#### **2. CLIP Templates**
- `clip_miyawaki_template.pth` (24.28 MB)
- `clip_vangerven_template.pth` (36.73 MB)

#### **3. Lite Templates**
- `lite_miyawaki_template.pth` (7.22 MB)

### 🚨 **Important Notes**

#### **Template Files Not Included in Git**
Template files are **NOT included** in the git repository due to their large size (7MB - 37MB each).

#### **How to Obtain Templates**
1. **Train your own templates**:
   ```python
   from cccv3.scripts.test_cccv3_ultimate import train_cccv3_templates
   
   # Train templates for all datasets
   train_cccv3_templates()
   ```

2. **Download from releases** (if available):
   - Check repository releases for pre-trained templates
   - Extract to `cccv3/model_templates/` directory

### 🔧 **Usage in CCCV3**

Templates are automatically loaded by CCCV3 models:
```python
from cccv3.scripts.test_cccv3_ultimate import CCCV3UltimateModel

# CCCV3 automatically loads appropriate template
model = CCCV3UltimateModel(dataset_name='miyawaki')
```

### 📊 **Template Specifications**

| Template | Dataset | Size (MB) | Architecture |
|----------|---------|-----------|--------------|
| attention_miyawaki | Miyawaki | 12.46 | Attention pathway |
| attention_mindbigdata | MindBigData | 28.65 | Attention pathway |
| attention_crell | Crell | 28.65 | Attention pathway |
| clip_miyawaki | Miyawaki | 24.28 | CLIP pathway |
| clip_vangerven | Vangerven | 36.73 | CLIP pathway |
| lite_miyawaki | Miyawaki | 7.22 | Lite pathway |

---

**📝 Note**: Template files are excluded from git due to size constraints. Please train or download templates separately.
