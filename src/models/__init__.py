"""
Neural Network Models for CortexFlow CCCV1-CCCV4 Release
========================================================

This module contains essential neural network architectures used by CCCV1-CCCV4.

Available Models:
    StandardBaselineCNN: Standard CNN baseline for comparison
    OptimizedMinDVis: MinD-Vis implementation for comparison
    OptimizedBrainDiffuser: Brain-Diffuser implementation for comparison

Note: CCCV1-CCCV4 models are located in their respective directories:
    - CCCV1: cccv1/src/models/
    - CCCV2: cccv2/src/models/  
    - CCCV3: cccv3/src/models/
    - CCCV4: cccv4/scripts/
"""

# Import essential models for comparison
from .baseline import StandardBaselineCNN
from .mind_vis import OptimizedMinDVis
from .brain_diffuser import OptimizedBrainDiffuser

__all__ = [
    'StandardBaselineCNN',
    'OptimizedMinDVis', 
    'OptimizedBrainDiffuser'
]
