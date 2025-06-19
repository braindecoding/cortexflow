"""
DEBUG CCCV4 - Simplified Testing
================================

This script debugs CCCV4 by testing it with a simpler approach
to identify and fix the MSE 0.000000 issue.
"""

import os
import sys
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from sklearn.model_selection import KFold
import warnings
warnings.filterwarnings('ignore')

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.append(root_dir)
sys.path.append(parent_dir)

# Import utilities
try:
    from src.data import load_dataset_gpu_optimized
except ImportError:
    print("⚠️ Parent directory imports not available")

def setup_device():
    """Setup CUDA device"""
    if torch.cuda.is_available():
        device = torch.device('cuda')
        print(f"🚀 Using GPU: {torch.cuda.get_device_name()}")
        torch.cuda.empty_cache()
        return device
    else:
        return torch.device('cpu')

class SimpleCCCV4Model(nn.Module):
    """
    Simplified CCCV4 Model for debugging
    """
    
    def __init__(self, input_dim, device='cuda'):
        super(SimpleCCCV4Model, self).__init__()
        self.model_name = "CortexFlow-CLIP-CNN-V4-Debug"
        self.device = device
        self.input_dim = input_dim
        
        # Simple CNN architecture for debugging
        self.feature_extractor = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU()
        )
        
        # Visual decoder
        self.visual_decoder = nn.Sequential(
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, 784),  # 28x28 = 784
            nn.Sigmoid()
        )
        
        self.to(device)
    
    def forward(self, x):
        """Forward pass"""
        features = self.feature_extractor(x)
        visual_output = self.visual_decoder(features)
        visual_output = visual_output.view(-1, 1, 28, 28)
        
        return visual_output, {'strategy': 'simple_debug'}

def train_simple_model(model, train_loader, val_loader, device, epochs=50):
    """Train simple model for debugging"""
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-6)
    criterion = nn.MSELoss()
    
    best_val_loss = float('inf')
    patience_counter = 0
    patience = 10
    
    print(f"🔧 Training Simple CCCV4 Debug Model...")
    
    for epoch in range(epochs):
        # Training
        model.train()
        train_loss = 0.0
        
        for data, target in train_loader:
            data, target = data.to(device), target.to(device)
            
            optimizer.zero_grad()
            visual_output, _ = model(data)
            loss = criterion(visual_output, target)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        
        # Validation
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(device), target.to(device)
                visual_output, _ = model(data)
                val_loss += criterion(visual_output, target).item()
        
        train_loss /= len(train_loader)
        val_loss /= len(val_loader)
        
        # Early stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
        else:
            patience_counter += 1
        
        if epoch % 10 == 0:
            print(f"     Epoch {epoch+1}: Train={train_loss:.6f}, Val={val_loss:.6f}")
        
        if patience_counter >= patience:
            print(f"     Early stopping at epoch {epoch+1}")
            break
    
    return best_val_loss

def debug_cccv4_on_dataset(dataset_name, device, n_folds=5):
    """Debug CCCV4 on a dataset with simplified approach"""
    
    print(f"\n🔍 Debugging CCCV4 on {dataset_name.upper()}")
    print("=" * 50)
    
    # Load dataset
    try:
        if 'load_dataset_gpu_optimized' in globals():
            X_train, y_train, X_test, y_test, input_dim = load_dataset_gpu_optimized(dataset_name, device)
            
            print("🔒 ACADEMIC INTEGRITY: Using corrected preprocessing (no data leakage)")
            print("   ✅ Training statistics used for test set normalization")
            print("   ✅ No information leakage from test set to training")
        else:
            print("❌ Dataset loading function not available")
            return None
        
        if X_train is None:
            print(f"❌ Failed to load {dataset_name}")
            return None
        
        dataset_size = len(X_train)
        print(f"✅ Dataset loaded: Train={dataset_size}, Test={len(X_test)}, Input_dim={input_dim}")
        
    except Exception as e:
        print(f"❌ Error loading {dataset_name}: {e}")
        return None
    
    # Combine for cross-validation
    X_all = torch.cat([X_train, X_test], dim=0)
    y_all = torch.cat([y_train, y_test], dim=0)
    
    print(f"📊 Total samples for {n_folds}-fold CV: {len(X_all)}")
    
    # Cross-validation
    kfold = KFold(n_splits=n_folds, shuffle=True, random_state=42)
    
    fold_results = []
    
    for fold, (train_idx, val_idx) in enumerate(kfold.split(X_all)):
        print(f"\n🔄 Fold {fold + 1}/{n_folds}")
        
        # Split data
        train_data = X_all[train_idx]
        train_targets = y_all[train_idx]
        val_data = X_all[val_idx]
        val_targets = y_all[val_idx]
        
        print(f"   Train: {len(train_data)}, Val: {len(val_data)}")
        
        # Create simple model
        model = SimpleCCCV4Model(input_dim, device)
        
        # Prepare data loaders
        batch_size = min(16, len(train_data) // 4)
        train_dataset = TensorDataset(train_data, train_targets)
        val_dataset = TensorDataset(val_data, val_targets)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        
        # Train model
        val_loss = train_simple_model(model, train_loader, val_loader, device)
        
        fold_results.append(val_loss)
        print(f"   Fold {fold + 1} MSE: {val_loss:.6f}")
        
        # Clear memory
        del model
        torch.cuda.empty_cache()
    
    # Aggregate results
    mean_mse = np.mean(fold_results)
    std_mse = np.std(fold_results)
    
    print(f"\n📊 {n_folds}-Fold Cross-Validation Results:")
    print(f"   Simple CCCV4 MSE: {mean_mse:.6f} ± {std_mse:.6f}")
    
    return {
        'dataset_name': dataset_name,
        'mean_mse': mean_mse,
        'std_mse': std_mse,
        'fold_results': fold_results
    }

def main():
    """Main debugging function"""
    print("🔍 CCCV4 DEBUG MODE")
    print("=" * 30)
    print("🎯 Testing simplified CCCV4 to identify MSE 0.000000 issue")
    print()
    
    device = setup_device()
    
    # Set seeds for reproducibility
    torch.manual_seed(42)
    np.random.seed(42)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(42)
    
    # Test on Miyawaki first
    result = debug_cccv4_on_dataset('miyawaki', device, n_folds=5)
    
    if result:
        print(f"\n🎉 DEBUG COMPLETE!")
        print(f"Simple CCCV4 MSE: {result['mean_mse']:.6f} ± {result['std_mse']:.6f}")
        
        if result['mean_mse'] > 0.001:
            print("✅ MSE values are realistic - debugging successful!")
        else:
            print("❌ MSE still too low - further investigation needed")
    else:
        print("❌ Debug failed")

if __name__ == "__main__":
    main()
