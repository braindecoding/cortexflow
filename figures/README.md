
# 🔒 ACADEMIC INTEGRITY COMPLIANCE NOTICE

**⚠️ CRITICAL UPDATE - 2025-06-19**

This document has been updated to ensure academic integrity compliance.

## **Methodology Correction**
- **Previous methodology**: Had data leakage (test set statistics used for test normalization)
- **Corrected methodology**: Uses training statistics for both training and test normalization
- **Impact**: Previous results were optimistically biased and invalid for publication

## **Result Status**
- **❌ Results before 2025-06-19 19:30**: INVALID (data leakage present)
- **✅ Results after 2025-06-19 19:30**: VALID (academic integrity compliant)

## **Publication Readiness**
- **Previous results**: NOT suitable for publication or peer review
- **Current results**: READY for journal submission and academic use

---

# CortexFlow CCCV1-CCCV4 Architecture Figures

This directory contains publication-ready architecture diagrams for CCCV1-CCCV4 models.

## Available Figures



## 🔬 **CORRECTED METHODOLOGY (Academic Integrity Compliant)**

### **Data Preprocessing**
- **Training Statistics**: Computed from training set only
- **Test Normalization**: Uses training statistics (eliminates data leakage)
- **Cross-Validation**: Preprocessing performed within each fold
- **Academic Integrity**: Verified and compliant

### **Key Improvements**
1. **Eliminated Data Leakage**: No test set information used in training
2. **Proper CV**: Preprocessing within folds prevents information leakage
3. **Reproducible**: All random seeds set for consistent results
4. **Publication Ready**: Methodology meets academic integrity standards

### **Previous vs Current Methodology**
| Aspect | Previous (INVALID) | Current (VALID) |
|--------|-------------------|-----------------|
| Test Normalization | Test set statistics | Training statistics |
| CV Preprocessing | Before split | Within each fold |
| Data Leakage | Present | Eliminated |
| Publication Status | Not suitable | Ready |


#### 1. Dataset Overview
- **Files**: `dataset_overview.png`, `dataset_overview.svg`
- **Description**: Overview of all datasets used in CCCV1-CCCV4
- **Content**: Miyawaki, Vangerven, MindBigData, Crell specifications

#### 2. Cross-Validation Methodology
- **Files**: `cv_methodology.png`, `cv_methodology.svg`
- **Description**: 10-fold cross-validation methodology diagram
- **Content**: Statistical validation approach used in CCCV1-CCCV4

#### 3. Evaluation Metrics
- **Files**: `evaluation_metrics.png`, `evaluation_metrics.svg`
- **Description**: Comprehensive evaluation metrics framework
- **Content**: MSE, PSNR, SSIM, LPIPS metrics explanation

#### 4. Training Pipeline
- **Files**: `training_pipeline.png`, `training_pipeline.svg`
- **Description**: Complete training pipeline for CCCV1-CCCV4
- **Content**: Data loading, training, validation, testing flow



## 🔬 **CORRECTED METHODOLOGY (Academic Integrity Compliant)**

### **Data Preprocessing**
- **Training Statistics**: Computed from training set only
- **Test Normalization**: Uses training statistics (eliminates data leakage)
- **Cross-Validation**: Preprocessing performed within each fold
- **Academic Integrity**: Verified and compliant

### **Key Improvements**
1. **Eliminated Data Leakage**: No test set information used in training
2. **Proper CV**: Preprocessing within folds prevents information leakage
3. **Reproducible**: All random seeds set for consistent results
4. **Publication Ready**: Methodology meets academic integrity standards

### **Previous vs Current Methodology**
| Aspect | Previous (INVALID) | Current (VALID) |
|--------|-------------------|-----------------|
| Test Normalization | Test set statistics | Training statistics |
| CV Preprocessing | Before split | Within each fold |
| Data Leakage | Present | Eliminated |
| Publication Status | Not suitable | Ready |


### Results and Analysis Figures

#### 5. Performance Table
- **Files**: `performance_table.png`, `performance_table.svg`
- **Description**: CCCV1-CCCV4 performance comparison
- **Content**: Inter-CCCV model comparison results

#### 6. Statistical Significance
- **Files**: `statistical_significance.png`, `statistical_significance.svg`
- **Description**: Statistical significance analysis
- **Content**: T-test results and confidence intervals

#### 7. Error Analysis
- **Files**: `error_analysis.png`, `error_analysis.svg`
- **Description**: Error analysis across datasets
- **Content**: MSE distribution and error patterns

#### 8. Research Contributions
- **Files**: `research_contributions.png`, `research_contributions.svg`
- **Description**: Summary of CCCV research contributions
- **Content**: CCCV1-CCCV4 innovations and achievements

## Usage Guidelines

### Academic Publications
- Use **SVG format** for vector graphics in LaTeX documents
- Use **PNG format** for presentations and web display
- All figures are publication-ready with 300 DPI resolution

### CCCV1-CCCV4 Documentation
- Figures support CCCV1-CCCV4 model documentation
- Focus on inter-CCCV model comparisons
- Methodology figures explain experimental setup

### Citation Information
When using these figures, please cite:
```
CortexFlow CCCV1-CCCV4: Meta-Adaptive Neural Decoding Framework
Advanced fMRI-to-Image Reconstruction with Reproducible Methodology
```

## Technical Specifications

- **Resolution**: 300 DPI for publication quality
- **Formats**: PNG (raster) and SVG (vector)
- **Style**: Publication-ready with serif fonts
- **Color Scheme**: Consistent across all figures
- **Mathematical Notation**: LaTeX-style formatting

## Note

This directory contains only figures relevant to CCCV1-CCCV4 models.
For SOTA baseline comparisons, switch to the 'sota-comparison' branch.

CCCV-specific architecture diagrams are located in their respective directories:
- CCCV1: `cccv1/docs/figures/`
- CCCV2: `cccv2/docs/figures/`
- CCCV3: `cccv3/docs/figures/`
- CCCV4: `cccv4/visualizations/`
