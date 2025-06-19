#!/usr/bin/env python3
"""
CortexFlow CCCV1-CCCV4 Training Script
=====================================

Clean training script for CortexFlow CCCV1-CCCV4 release.

Usage:
    python train_cccv.py --model cccv4 --dataset miyawaki
    python train_cccv.py --model cccv3 --dataset vangerven
    python train_cccv.py --model cccv2 --dataset mindbigdata
    python train_cccv.py --model cccv1 --dataset crell

Available Models:
    - cccv1: Foundation model
    - cccv2: Enhanced model
    - cccv3: Ultimate adaptive model
    - cccv4: Meta-adaptive intelligence (recommended)

Available Datasets:
    - miyawaki: Visual cortex fMRI (107 samples, 967 features)
    - vangerven: Visual stimuli fMRI (90 samples, 3092 features)
    - mindbigdata: Large-scale neural data (1080 samples, 3092 features)
    - crell: Medium complexity dataset (576 samples, 3092 features)
"""

import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description='CortexFlow CCCV1-CCCV4 Training')
    parser.add_argument('--model', choices=['cccv1', 'cccv2', 'cccv3', 'cccv4'],
                       default='cccv4', help='Model version to use')
    parser.add_argument('--dataset', choices=['miyawaki', 'vangerven', 'mindbigdata', 'crell'],
                       required=True, help='Dataset to train on')

    args = parser.parse_args()

    print(f"CortexFlow {args.model.upper()} Training")
    print(f"Dataset: {args.dataset.upper()}")
    print("=" * 50)

    # Route to appropriate CCCV training script
    if args.model == 'cccv4':
        print("Using CCCV4 Meta-Adaptive (Recommended)")
        print("Running: cccv4/scripts/test_cccv4_simplified.py")
        os.system(f"python cccv4/scripts/test_cccv4_simplified.py")

    elif args.model == 'cccv3':
        print("Using CCCV3 Ultimate Adaptive")
        print("Running: cccv3/scripts/test_cccv3_ultimate.py")
        os.system(f"python cccv3/scripts/test_cccv3_ultimate.py")

    elif args.model == 'cccv2':
        print("Using CCCV2 Enhanced")
        print("Running: cccv2/scripts/final_cccv2_integration.py")
        os.system(f"python cccv2/scripts/final_cccv2_integration.py")

    elif args.model == 'cccv1':
        print("Using CCCV1 Foundation")
        print("Running: cccv1/scripts/train_cccv1.py")
        os.system(f"python cccv1/scripts/train_cccv1.py")

    print(f"\n{args.model.upper()} training completed!")
    print(f"Check respective results directories for outputs")

if __name__ == "__main__":
    main()