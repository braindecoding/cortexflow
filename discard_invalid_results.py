"""
Discard Invalid Results - Academic Integrity Compliance
======================================================

This script identifies and removes all results generated before the
academic integrity fixes were implemented. These results are invalid
due to data leakage and must be discarded.

CRITICAL: All results before the academic integrity fix (2025-06-19 19:30)
are INVALID and must be removed to prevent publication of biased results.

ACTIONS PERFORMED:
1. Identify all result files and directories
2. Create backup of invalid results for reference
3. Remove invalid results from active directories
4. Generate report of discarded results
5. Update documentation to reflect methodology correction
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import glob


def find_invalid_result_files():
    """
    Find all result files that were generated before academic integrity fix.
    
    Returns:
        dict: Dictionary of invalid files categorized by type
    """
    
    print("🔍 IDENTIFYING INVALID RESULT FILES")
    print("=" * 50)
    
    invalid_files = {
        'result_directories': [],
        'json_results': [],
        'model_files': [],
        'log_files': [],
        'figure_files': [],
        'documentation_with_results': [],
        'backup_files': []
    }
    
    # Define patterns for different types of result files
    result_patterns = {
        'result_directories': [
            'cccv*/results/*',
            'results/*',
            'outputs/*',
            'logs/*',
            'experiments/*'
        ],
        'json_results': [
            '*.json',
            'cccv*/**/*.json',
            '**/results*.json',
            '**/validation*.json',
            '**/breakthrough*.json'
        ],
        'model_files': [
            '*.pth',
            '*.pt',
            '*.ckpt',
            'cccv*/**/*.pth',
            'models/*',
            'checkpoints/*'
        ],
        'log_files': [
            '*.log',
            'training_logs/*',
            'validation_logs/*',
            'cccv*/**/*.log'
        ],
        'figure_files': [
            'figures/*.png',
            'figures/*.jpg',
            'figures/*.pdf',
            'plots/*',
            'visualizations/*'
        ],
        'documentation_with_results': [
            'cccv*/results/*.md',
            '**/breakthrough*.md',
            '**/summary*.md',
            '**/performance*.md'
        ]
    }
    
    # Search for files
    for category, patterns in result_patterns.items():
        print(f"  Searching {category}...")
        
        for pattern in patterns:
            for file_path in glob.glob(pattern, recursive=True):
                path_obj = Path(file_path)
                
                # Skip if it's a directory and we're looking for files
                if path_obj.is_dir() and category != 'result_directories':
                    continue
                
                # Skip if it's a file and we're looking for directories
                if path_obj.is_file() and category == 'result_directories':
                    continue
                
                # Skip backup files created today (they're from the fix)
                if 'backup_20250619' in str(path_obj):
                    invalid_files['backup_files'].append(str(path_obj))
                    continue
                
                # Skip the academic integrity validation report (it's valid)
                if 'academic_integrity_validation_report.json' in str(path_obj):
                    continue
                
                # Skip files created after the fix
                try:
                    if path_obj.exists():
                        # Check modification time
                        mod_time = datetime.fromtimestamp(path_obj.stat().st_mtime)
                        fix_time = datetime(2025, 6, 19, 19, 30)  # Academic integrity fix time
                        
                        if mod_time < fix_time:
                            invalid_files[category].append(str(path_obj))
                        else:
                            print(f"    ✅ Keeping recent file: {path_obj}")
                except Exception as e:
                    # If we can't check time, assume it's invalid to be safe
                    invalid_files[category].append(str(path_obj))
    
    return invalid_files


def create_invalid_results_backup(invalid_files):
    """
    Create backup of invalid results before deletion.
    
    Args:
        invalid_files: Dictionary of invalid files to backup
        
    Returns:
        str: Path to backup directory
    """
    
    print("\n📦 CREATING BACKUP OF INVALID RESULTS")
    print("=" * 50)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"invalid_results_backup_{timestamp}")
    backup_dir.mkdir(exist_ok=True)
    
    backup_count = 0
    
    for category, files in invalid_files.items():
        if not files:
            continue
            
        category_backup_dir = backup_dir / category
        category_backup_dir.mkdir(exist_ok=True)
        
        print(f"  Backing up {category}: {len(files)} items")
        
        for file_path in files:
            try:
                source_path = Path(file_path)
                if not source_path.exists():
                    continue
                
                # Create relative path structure in backup
                if source_path.is_absolute():
                    relative_path = source_path.relative_to(Path.cwd())
                else:
                    relative_path = source_path
                
                backup_file_path = category_backup_dir / relative_path.name
                
                # Ensure unique names
                counter = 1
                original_backup_path = backup_file_path
                while backup_file_path.exists():
                    backup_file_path = original_backup_path.with_stem(
                        f"{original_backup_path.stem}_{counter}"
                    )
                    counter += 1
                
                if source_path.is_file():
                    backup_file_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_path, backup_file_path)
                elif source_path.is_dir():
                    shutil.copytree(source_path, backup_file_path, dirs_exist_ok=True)
                
                backup_count += 1
                
            except Exception as e:
                print(f"    ⚠️ Could not backup {file_path}: {e}")
    
    print(f"  ✅ Backed up {backup_count} items to {backup_dir}")
    return str(backup_dir)


def remove_invalid_results(invalid_files):
    """
    Remove invalid result files and directories.
    
    Args:
        invalid_files: Dictionary of invalid files to remove
        
    Returns:
        dict: Summary of removal actions
    """
    
    print("\n🗑️ REMOVING INVALID RESULTS")
    print("=" * 50)
    
    removal_summary = {
        'removed_files': 0,
        'removed_directories': 0,
        'failed_removals': 0,
        'errors': []
    }
    
    # Remove files first, then directories
    all_files = []
    all_dirs = []
    
    for category, files in invalid_files.items():
        if category == 'backup_files':
            continue  # Don't remove backup files
            
        for file_path in files:
            path_obj = Path(file_path)
            if path_obj.is_file():
                all_files.append(path_obj)
            elif path_obj.is_dir():
                all_dirs.append(path_obj)
    
    # Remove files
    print(f"  Removing {len(all_files)} files...")
    for file_path in all_files:
        try:
            if file_path.exists():
                file_path.unlink()
                removal_summary['removed_files'] += 1
                print(f"    ✅ Removed: {file_path}")
        except Exception as e:
            removal_summary['failed_removals'] += 1
            removal_summary['errors'].append(f"Failed to remove {file_path}: {e}")
            print(f"    ❌ Failed to remove: {file_path} - {e}")
    
    # Remove directories (in reverse order to handle nested directories)
    print(f"  Removing {len(all_dirs)} directories...")
    for dir_path in sorted(all_dirs, key=lambda x: len(str(x)), reverse=True):
        try:
            if dir_path.exists() and dir_path.is_dir():
                shutil.rmtree(dir_path)
                removal_summary['removed_directories'] += 1
                print(f"    ✅ Removed directory: {dir_path}")
        except Exception as e:
            removal_summary['failed_removals'] += 1
            removal_summary['errors'].append(f"Failed to remove {dir_path}: {e}")
            print(f"    ❌ Failed to remove directory: {dir_path} - {e}")
    
    return removal_summary


def generate_discard_report(invalid_files, backup_dir, removal_summary):
    """
    Generate comprehensive report of discarded results.
    
    Args:
        invalid_files: Dictionary of invalid files
        backup_dir: Path to backup directory
        removal_summary: Summary of removal actions
        
    Returns:
        str: Path to report file
    """
    
    print("\n📄 GENERATING DISCARD REPORT")
    print("=" * 50)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = {
        'discard_timestamp': timestamp,
        'reason': 'Academic integrity compliance - data leakage elimination',
        'fix_implemented': '2025-06-19 19:30:00',
        'invalid_files_summary': {
            category: len(files) for category, files in invalid_files.items()
        },
        'invalid_files_detail': invalid_files,
        'backup_location': backup_dir,
        'removal_summary': removal_summary,
        'academic_integrity_status': {
            'previous_results': 'INVALID - Data leakage present',
            'current_methodology': 'VALID - Academic integrity compliant',
            'action_required': 'Re-run all experiments with corrected methodology'
        },
        'impact_assessment': {
            'affected_experiments': 'All CCCV1-CCCV4 experiments before fix',
            'affected_datasets': ['miyawaki', 'vangerven', 'mindbigdata', 'crell'],
            'bias_type': 'Optimistic bias due to test set information leakage',
            'publication_status': 'Previous results NOT suitable for publication'
        }
    }
    
    report_file = Path("invalid_results_discard_report.json")
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"  ✅ Report saved to: {report_file}")
    
    # Also create human-readable summary
    summary_file = Path("INVALID_RESULTS_SUMMARY.md")
    
    summary_content = f"""# INVALID RESULTS DISCARDED - ACADEMIC INTEGRITY COMPLIANCE

## 🚨 CRITICAL NOTICE

**ALL RESULTS GENERATED BEFORE 2025-06-19 19:30 HAVE BEEN DISCARDED**

### **Reason for Discard**
- **Data Leakage Identified**: Test set statistics used for test set normalization
- **Academic Integrity Violation**: Methodology caused optimistic bias
- **Publication Risk**: Results not suitable for peer review or journal submission

### **Files Discarded**
- **Result Directories**: {len(invalid_files['result_directories'])} directories
- **JSON Results**: {len(invalid_files['json_results'])} files
- **Model Files**: {len(invalid_files['model_files'])} files
- **Log Files**: {len(invalid_files['log_files'])} files
- **Figure Files**: {len(invalid_files['figure_files'])} files
- **Documentation**: {len(invalid_files['documentation_with_results'])} files

### **Backup Location**
All discarded results have been backed up to: `{backup_dir}`

### **Removal Summary**
- **Files Removed**: {removal_summary['removed_files']}
- **Directories Removed**: {removal_summary['removed_directories']}
- **Failed Removals**: {removal_summary['failed_removals']}

### **Academic Integrity Status**
- **Previous Methodology**: ❌ INVALID (data leakage present)
- **Current Methodology**: ✅ VALID (academic integrity compliant)
- **Publication Status**: ✅ READY (after re-running experiments)

### **Required Actions**
1. ✅ **Discard Invalid Results**: COMPLETED
2. ⏳ **Re-run All Experiments**: REQUIRED with corrected methodology
3. ⏳ **Update Documentation**: REQUIRED with new results
4. ⏳ **Inform Collaborators**: REQUIRED about methodology correction

### **Impact Assessment**
- **Affected Experiments**: All CCCV1-CCCV4 experiments
- **Affected Datasets**: Miyawaki, Vangerven, MindBigData, Crell
- **Bias Type**: Optimistic bias (results likely better than reality)
- **Magnitude**: Unknown (requires re-evaluation with corrected methodology)

---

**⚠️ IMPORTANT**: Do not use any results from backup directory for publication.
All future results must be generated using the corrected methodology.

**Generated**: {timestamp}
"""
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"  ✅ Summary saved to: {summary_file}")
    
    return str(report_file)


def main():
    """
    Main function to discard invalid results.
    """
    
    print("🚨 DISCARDING INVALID RESULTS - ACADEMIC INTEGRITY COMPLIANCE")
    print("=" * 70)
    print("This will identify and remove all results generated before the")
    print("academic integrity fix to prevent publication of biased results.")
    print()
    
    # Find invalid files
    invalid_files = find_invalid_result_files()
    
    # Count total invalid items
    total_invalid = sum(len(files) for files in invalid_files.values())
    
    if total_invalid == 0:
        print("✅ No invalid result files found!")
        print("   All existing results appear to be from after the academic integrity fix.")
        return
    
    print(f"\n📊 INVALID RESULTS SUMMARY:")
    for category, files in invalid_files.items():
        if files:
            print(f"  {category}: {len(files)} items")
    print(f"  TOTAL INVALID ITEMS: {total_invalid}")
    
    # Confirm discard
    print(f"\n⚠️  WARNING: This will permanently remove {total_invalid} invalid result items!")
    print("   (Backup will be created first)")
    response = input("\n🗑️ Proceed with discarding invalid results? (y/N): ").strip().lower()
    
    if response != 'y':
        print("❌ Discard cancelled")
        return
    
    # Create backup
    backup_dir = create_invalid_results_backup(invalid_files)
    
    # Remove invalid results
    removal_summary = remove_invalid_results(invalid_files)
    
    # Generate report
    report_file = generate_discard_report(invalid_files, backup_dir, removal_summary)
    
    # Final summary
    print("\n" + "=" * 70)
    print("🏆 INVALID RESULTS DISCARD COMPLETED")
    print("=" * 70)
    print(f"✅ Files removed: {removal_summary['removed_files']}")
    print(f"✅ Directories removed: {removal_summary['removed_directories']}")
    print(f"❌ Failed removals: {removal_summary['failed_removals']}")
    print(f"📦 Backup created: {backup_dir}")
    print(f"📄 Report saved: {report_file}")
    
    if removal_summary['failed_removals'] == 0:
        print(f"\n🎉 ALL INVALID RESULTS SUCCESSFULLY DISCARDED!")
        print(f"✅ Repository is now clean of biased results")
        print(f"✅ Ready for re-running experiments with corrected methodology")
    else:
        print(f"\n⚠️  {removal_summary['failed_removals']} items could not be removed")
        print(f"❌ Please manually review and remove failed items")
    
    print(f"\n🚨 CRITICAL: All future experiments must use the corrected methodology!")


if __name__ == "__main__":
    main()
