# CortexFlow CCCV1-CCCV4 Architecture Figures

This directory contains publication-ready architecture diagrams for CCCV1-CCCV4 models and baseline comparison methods.

## Available Figures

### Baseline Comparison Architectures

#### 1. Brain-Diffuser Architecture
- **Files**: `brain_diffuser_architecture.png`, `brain_diffuser_architecture.svg`
- **Description**: State-of-the-art diffusion approach for neural decoding
- **Key Features**:
  - SiLU activation and LayerNorm
  - 10 timesteps with beta linear schedule
  - Iterative denoising inference
- **Usage**: Baseline comparison for CCCV1-CCCV4

#### 2. MinD-Vis Architecture
- **Files**: `mindvis_architecture.png`, `mindvis_architecture.svg`
- **Description**: SOTA conditional diffusion (CVPR 2023)
- **Key Features**:
  - Sparse masked modeling with 15% masking
  - Conditional diffusion decoder
  - Noise injection for diffusion simulation
- **Usage**: Baseline comparison for CCCV1-CCCV4

#### 3. CortexFlow-Lite Architecture
- **Files**: `cortexflow_lite_architecture.png`, `cortexflow_lite_architecture.svg`
- **Description**: Lightweight baseline architecture
- **Key Features**:
  - BatchNorm1d normalization for stability
  - Dropout (0.2, 0.15) for optimal regularization
  - Architecture: input → 512 → 256 → 512 → 784 (output)
- **Usage**: Baseline comparison for CCCV1-CCCV4

### Methodology Figures

#### 4. Dataset Overview
- **Files**: `dataset_overview.png`, `dataset_overview.svg`
- **Description**: Overview of all datasets used in CCCV1-CCCV4
- **Content**: Miyawaki, Vangerven, MindBigData, Crell specifications

#### 5. Cross-Validation Methodology
- **Files**: `cv_methodology.png`, `cv_methodology.svg`
- **Description**: 5-fold cross-validation methodology diagram
- **Content**: Statistical validation approach used in CCCV1-CCCV4

#### 6. Evaluation Metrics
- **Files**: `evaluation_metrics.png`, `evaluation_metrics.svg`
- **Description**: Comprehensive evaluation metrics framework
- **Content**: MSE, PSNR, SSIM, LPIPS metrics explanation

#### 7. Training Pipeline
- **Files**: `training_pipeline.png`, `training_pipeline.svg`
- **Description**: Complete training pipeline for CCCV1-CCCV4
- **Content**: Data loading, training, validation, testing flow

### Results and Analysis Figures

#### 8. Performance Table
- **Files**: `performance_table.png`, `performance_table.svg`
- **Description**: Performance comparison table
- **Content**: CCCV1-CCCV4 vs baseline methods

#### 9. Statistical Significance
- **Files**: `statistical_significance.png`, `statistical_significance.svg`
- **Description**: Statistical significance analysis
- **Content**: T-test results and confidence intervals

#### 10. Error Analysis
- **Files**: `error_analysis.png`, `error_analysis.svg`
- **Description**: Error analysis across datasets
- **Content**: MSE distribution and error patterns

#### 11. Research Contributions
- **Files**: `research_contributions.png`, `research_contributions.svg`
- **Description**: Summary of research contributions
- **Content**: CCCV1-CCCV4 innovations and achievements

## Usage Guidelines

### Academic Publications
- Use **SVG format** for vector graphics in LaTeX documents
- Use **PNG format** for presentations and web display
- All figures are publication-ready with 300 DPI resolution

### CCCV1-CCCV4 Documentation
- Figures support CCCV1-CCCV4 model documentation
- Baseline comparisons show performance context
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

This directory contains only figures relevant to CCCV1-CCCV4 release.
CCCV-specific architecture diagrams are located in their respective directories:
- CCCV1: `cccv1/docs/figures/`
- CCCV2: `cccv2/docs/figures/`
- CCCV3: `cccv3/docs/figures/`
- CCCV4: `cccv4/visualizations/`
