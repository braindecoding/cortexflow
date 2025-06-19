"""
Cleanup SOTA Baselines for CCCV-Focused Release Branch
=====================================================

Remove all SOTA baseline implementations and references to focus
the release branch purely on CCCV1-CCCV4 models.

Strategy:
1. Remove SOTA baseline model files (Brain-Diffuser, MinD-Vis, StandardBaselineCNN)
2. Remove SOTA comparison code from CCCV scripts
3. Update imports and references
4. Clean up test files that reference SOTA models
5. Update documentation to focus on CCCV only
6. Keep only CCCV1-CCCV4 essential functionality
"""

import os
import shutil
from pathlib import Path

def remove_sota_model_files():
    """Remove SOTA baseline model implementation files"""
    
    print("🗑️ REMOVING SOTA BASELINE MODEL FILES:")
    print("=" * 50)
    
    # SOTA model files to remove
    sota_files = [
        'src/models/brain_diffuser.py',
        'src/models/mind_vis.py', 
        'src/models/baseline.py'
    ]
    
    for file_path in sota_files:
        if os.path.exists(file_path):
            print(f"   Removing: {file_path}")
            os.remove(file_path)
        else:
            print(f"   Not found: {file_path}")

def update_src_models_init():
    """Update src/models/__init__.py to remove SOTA imports"""
    
    print("\n📝 UPDATING src/models/__init__.py:")
    print("=" * 40)
    
    new_init_content = '''"""
Neural Network Models for CortexFlow CCCV1-CCCV4 Release
========================================================

This module contains only CCCV-specific models.
SOTA baseline models have been moved to a separate branch.

CCCV Models are located in their respective directories:
    - CCCV1: cccv1/src/models/
    - CCCV2: cccv2/src/models/  
    - CCCV3: cccv3/src/models/
    - CCCV4: cccv4/scripts/

Note: For SOTA comparisons, switch to the 'sota-comparison' branch.
"""

# No baseline models in CCCV-focused release
__all__ = []
'''
    
    init_path = Path("src/models/__init__.py")
    if init_path.exists():
        with open(init_path, 'w') as f:
            f.write(new_init_content)
        print("   ✅ Updated: src/models/__init__.py")
    else:
        print("   ❌ src/models/__init__.py not found")

def remove_sota_references_from_cccv_scripts():
    """Remove SOTA comparison code from CCCV scripts"""
    
    print("\n🔧 REMOVING SOTA REFERENCES FROM CCCV SCRIPTS:")
    print("=" * 50)
    
    # Files that contain SOTA comparisons
    files_to_clean = [
        'cccv3/scripts/test_cccv3_adaptive.py',
        'cccv3/scripts/test_cccv3_ensemble.py', 
        'cccv4/scripts/test_cccv4_comprehensive.py',
        'cccv4/scripts/test_cccv4_simplified.py'
    ]
    
    for file_path in files_to_clean:
        if os.path.exists(file_path):
            print(f"   Processing: {file_path}")
            # We'll update these files to remove baseline comparisons
            # For now, just mark them for manual review
            print(f"   ⚠️  Manual review needed: {file_path}")
        else:
            print(f"   Not found: {file_path}")

def update_test_cccv():
    """Update tests/test_cccv.py to remove SOTA model tests"""
    
    print("\n📝 UPDATING tests/test_cccv.py:")
    print("=" * 40)
    
    test_file = Path("tests/test_cccv.py")
    if test_file.exists():
        # Read current content
        with open(test_file, 'r') as f:
            content = f.read()
        
        # Remove baseline model test
        lines = content.split('\n')
        new_lines = []
        skip_function = False
        
        for line in lines:
            if 'def test_baseline_models():' in line:
                skip_function = True
                continue
            elif skip_function and line.startswith('def '):
                skip_function = False
            elif skip_function:
                continue
            
            # Remove baseline model imports and references
            if 'StandardBaselineCNN, OptimizedMinDVis, OptimizedBrainDiffuser' in line:
                continue
            elif 'from src.models import' in line and 'StandardBaselineCNN' in line:
                continue
            elif '("Baseline Models", test_baseline_models)' in line:
                continue
                
            new_lines.append(line)
        
        # Write updated content
        with open(test_file, 'w') as f:
            f.write('\n'.join(new_lines))
        
        print("   ✅ Updated: tests/test_cccv.py")
    else:
        print("   ❌ tests/test_cccv.py not found")

def update_figures_readme():
    """Update figures/README.md to focus on CCCV only"""
    
    print("\n📝 UPDATING figures/README.md:")
    print("=" * 40)
    
    new_readme_content = '''# CortexFlow CCCV1-CCCV4 Architecture Figures

This directory contains publication-ready architecture diagrams for CCCV1-CCCV4 models.

## Available Figures

### Methodology Figures

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
'''
    
    readme_path = Path("figures/README.md")
    if readme_path.exists():
        with open(readme_path, 'w') as f:
            f.write(new_readme_content)
        print("   ✅ Updated: figures/README.md")
    else:
        print("   ❌ figures/README.md not found")

def remove_sota_figures():
    """Remove SOTA baseline architecture figures"""
    
    print("\n🗑️ REMOVING SOTA BASELINE FIGURES:")
    print("=" * 40)
    
    # SOTA figures to remove
    sota_figures = [
        'figures/brain_diffuser_architecture.png',
        'figures/brain_diffuser_architecture.svg',
        'figures/mindvis_architecture.png',
        'figures/mindvis_architecture.svg',
        'figures/cortexflow_lite_architecture.png',
        'figures/cortexflow_lite_architecture.svg'
    ]
    
    for figure in sota_figures:
        if os.path.exists(figure):
            print(f"   Removing: {figure}")
            os.remove(figure)
        else:
            print(f"   Not found: {figure}")

def update_readme_main():
    """Update main README.md to focus on CCCV only"""
    
    print("\n📝 UPDATING main README.md:")
    print("=" * 40)
    
    # We'll need to remove SOTA comparison sections
    # For now, just mark for manual review
    print("   ⚠️  Manual review needed: README.md")
    print("   - Remove SOTA comparison sections")
    print("   - Focus on CCCV1-CCCV4 only")
    print("   - Update performance tables")

def verify_cleanup():
    """Verify cleanup results"""
    
    print("\n🔍 VERIFYING CLEANUP RESULTS:")
    print("=" * 40)
    
    # Check if SOTA files are removed
    sota_files = [
        'src/models/brain_diffuser.py',
        'src/models/mind_vis.py', 
        'src/models/baseline.py'
    ]
    
    remaining_files = []
    for file_path in sota_files:
        if os.path.exists(file_path):
            remaining_files.append(file_path)
    
    if remaining_files:
        print(f"   ⚠️  Remaining SOTA files: {remaining_files}")
    else:
        print("   ✅ All SOTA model files removed")
    
    # Check remaining structure
    print(f"\n📁 Remaining src/models structure:")
    if os.path.exists('src/models'):
        for item in os.listdir('src/models'):
            print(f"   - {item}")
    
    print(f"\n📁 Remaining figures:")
    if os.path.exists('figures'):
        figure_count = len([f for f in os.listdir('figures') if f.endswith(('.png', '.svg'))])
        print(f"   - {figure_count} figure files remaining")

def main():
    """Main cleanup function"""
    
    print("🎯 CCCV-FOCUSED RELEASE BRANCH CLEANUP")
    print("=" * 50)
    print("🎯 Goal: Remove SOTA baselines, focus only on CCCV1-CCCV4")
    print()
    
    # Remove SOTA model files
    remove_sota_model_files()
    
    # Update src/models/__init__.py
    update_src_models_init()
    
    # Remove SOTA figures
    remove_sota_figures()
    
    # Update figures README
    update_figures_readme()
    
    # Update test file
    update_test_cccv()
    
    # Mark files for manual review
    remove_sota_references_from_cccv_scripts()
    update_readme_main()
    
    # Verify cleanup
    verify_cleanup()
    
    print("\n🎉 CCCV-FOCUSED CLEANUP COMPLETE!")
    print("=" * 50)
    print("✅ Removed SOTA baseline model files")
    print("✅ Updated imports and references") 
    print("✅ Removed SOTA architecture figures")
    print("✅ Updated documentation")
    print("✅ Cleaned test files")
    print()
    print("⚠️  MANUAL REVIEW NEEDED:")
    print("- CCCV scripts: Remove baseline comparison code")
    print("- README.md: Remove SOTA comparison sections")
    print("- Performance tables: Focus on inter-CCCV comparisons")
    print()
    print("🚀 Branch now focused on CCCV1-CCCV4 only!")
    print("💡 Create 'sota-comparison' branch for baseline comparisons")

if __name__ == "__main__":
    main()
