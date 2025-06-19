#!/usr/bin/env python3
"""
CortexFlow CCCV1-CCCV4 Training Script
=====================================

Unified training script for CortexFlow CCCV1-CCCV4 models with 10-fold cross-validation.
All results saved to results/{model}/{dataset}/ with comprehensive evaluation metrics.

Usage:
    # Train specific model on specific dataset
    python train_cccv.py --model cccv4 --dataset miyawaki
    python train_cccv.py --model cccv1 --dataset vangerven

    # Train model on all datasets (10-fold CV each)
    python train_cccv.py --model cccv4 --dataset all
    python train_cccv.py --model cccv1 --dataset all

Available Models:
    - cccv1: Foundation model (Overall best performer)
    - cccv2: Enhanced model (Balanced performance)
    - cccv3: Ultimate adaptive model (Complex datasets)
    - cccv4: Meta-adaptive intelligence (Automatic selection)

Available Datasets:
    - miyawaki: Visual cortex fMRI (119 samples, 967 features)
    - vangerven: Visual stimuli fMRI (100 samples, 3092 features)
    - mindbigdata: Large-scale neural data (1200 samples, 3092 features)
    - crell: Medium complexity dataset (640 samples, 3092 features)
    - all: Run on all 4 datasets sequentially

Results Structure:
    results/{model}/{dataset}/
    ├── models/         # 10 trained model files (fold_1_best_model.pth, ...)
    ├── training_info/  # Training logs, hyperparameters, CV summary
    ├── visualizations/ # Target vs reconstruction comparisons
    └── evaluations/    # 7 metrics: MSE, PSNR, SSIM, LPIPS, PixCorr, Inception Distance, CLIP Similarity
"""

import argparse
import subprocess

def run_cccv_training(model, dataset):
    """Run training for specific model and dataset combination"""

    print(f"\n🚀 CortexFlow {model.upper()} Training")
    print(f"📊 Dataset: {dataset.upper()}")
    print(f"🔄 Method: 10-Fold Cross-Validation")
    print("=" * 60)

    # Route to appropriate CCCV training script with 10-fold CV
    if model == 'cccv4':
        print("🧠 Using CCCV4 Meta-Adaptive (Recommended)")
        if dataset == 'all':
            print("📊 Running on all 4 datasets...")
            cmd = f"python cccv4/scripts/test_cccv4_simplified.py --dataset all"
        else:
            cmd = f"python cccv4/scripts/test_cccv4_simplified.py --dataset {dataset}"

    elif model == 'cccv3':
        print("🎯 Using CCCV3 Ultimate Adaptive")
        if dataset == 'all':
            print("📊 Running on all 4 datasets...")
            for ds in ['miyawaki', 'vangerven', 'mindbigdata', 'crell']:
                cmd = f"python cccv3/scripts/train_with_cv.py --dataset {ds}"
                print(f"   Running: {cmd}")
                subprocess.run(cmd, shell=True)
            return
        else:
            cmd = f"python cccv3/scripts/train_with_cv.py --dataset {dataset}"

    elif model == 'cccv2':
        print("⚡ Using CCCV2 Enhanced")
        if dataset == 'all':
            print("📊 Running on all 4 datasets...")
            for ds in ['miyawaki', 'vangerven', 'mindbigdata', 'crell']:
                cmd = f"python cccv2/scripts/train_with_cv.py --dataset {ds}"
                print(f"   Running: {cmd}")
                subprocess.run(cmd, shell=True)
            return
        else:
            cmd = f"python cccv2/scripts/train_with_cv.py --dataset {dataset}"

    elif model == 'cccv1':
        print("🏅 Using CCCV1 Foundation")
        if dataset == 'all':
            print("📊 Running on all 4 datasets...")
            for ds in ['miyawaki', 'vangerven', 'mindbigdata', 'crell']:
                cmd = f"python cccv1/scripts/train_with_cv.py --dataset {ds}"
                print(f"   Running: {cmd}")
                subprocess.run(cmd, shell=True)
            return
        else:
            cmd = f"python cccv1/scripts/train_with_cv.py --dataset {dataset}"

    print(f"🔧 Executing: {cmd}")
    result = subprocess.run(cmd, shell=True)

    if result.returncode == 0:
        print(f"\n✅ {model.upper()} training completed successfully!")
        print(f"📁 Results saved to: results/{model}/{dataset}/")
        print(f"📊 Check evaluations/ for comprehensive metrics")
        print(f"🎨 Check visualizations/ for target vs reconstruction comparisons")
    else:
        print(f"\n❌ {model.upper()} training failed!")
        print(f"🔍 Check logs for error details")

def main():
    parser = argparse.ArgumentParser(
        description='CortexFlow CCCV1-CCCV4 Training with 10-Fold Cross-Validation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Train CCCV4 on Miyawaki dataset
    python train_cccv.py --model cccv4 --dataset miyawaki

    # Train CCCV1 on all datasets
    python train_cccv.py --model cccv1 --dataset all

    # Train all models on Vangerven dataset
    python train_cccv.py --model cccv1 --dataset vangerven
    python train_cccv.py --model cccv2 --dataset vangerven
    python train_cccv.py --model cccv3 --dataset vangerven
    python train_cccv.py --model cccv4 --dataset vangerven
        """
    )

    parser.add_argument('--model',
                       choices=['cccv1', 'cccv2', 'cccv3', 'cccv4'],
                       default='cccv4',
                       help='Model version to use (default: cccv4)')
    parser.add_argument('--dataset',
                       choices=['miyawaki', 'vangerven', 'mindbigdata', 'crell', 'all'],
                       required=True,
                       help='Dataset to train on (use "all" for all datasets)')

    args = parser.parse_args()

    print("🧠 CortexFlow Neural Decoding Framework")
    print("🎯 Repository Focus: CCCV1-CCCV4 Models Only")
    print("🔬 Academic Integrity Compliant Methodology")
    print("📊 10-Fold Cross-Validation on All Datasets")

    if args.dataset == 'all':
        print(f"\n🚀 Training {args.model.upper()} on ALL 4 datasets...")
        datasets = ['miyawaki', 'vangerven', 'mindbigdata', 'crell']
        for i, dataset in enumerate(datasets, 1):
            print(f"\n📊 Dataset {i}/4: {dataset.upper()}")
            run_cccv_training(args.model, dataset)

        print(f"\n🎉 ALL TRAINING COMPLETED!")
        print(f"📁 Results for all datasets saved to: results/{args.model}/")

    else:
        run_cccv_training(args.model, args.dataset)

if __name__ == "__main__":
    main()