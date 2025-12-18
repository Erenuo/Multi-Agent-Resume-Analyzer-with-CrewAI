"""
Windows Compatibility Patch for CrewAI - Direct Fix
====================================================
Patches system_events.py to work on Windows by using getattr for signals.
"""

import os
import sys
import re

def patch_crewai():
    """Patch CrewAI to work on Windows by fixing signal imports."""
    
    # Find CrewAI path manually
    crewai_path = None
    for path in sys.path:
        if 'site-packages' in path:
            potential_path = os.path.join(path, 'crewai')
            if os.path.exists(potential_path):
                crewai_path = potential_path
                break
    
    if not crewai_path:
        # Try the venv path directly
        script_dir = os.path.dirname(os.path.abspath(__file__))
        crewai_path = os.path.join(script_dir, 'venv', 'Lib', 'site-packages', 'crewai')
    
    if not os.path.exists(crewai_path):
        print(f"Error: Could not find CrewAI package at {crewai_path}")
        return False
    
    events_file = os.path.join(crewai_path, 'events', 'types', 'system_events.py')
    
    if not os.path.exists(events_file):
        print(f"Error: Could not find {events_file}")
        return False
    
    print(f"Patching: {events_file}")
    
    with open(events_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already patched
    if 'getattr(signal' in content:
        print("File is already patched!")
        return True
    
    # Create backup
    backup_file = events_file + '.backup'
    if not os.path.exists(backup_file):
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Backup created: {backup_file}")
    
    # Replace all signal.SIGXXX with getattr(signal, 'SIGXXX', signal.SIGTERM)
    # But keep SIGINT and SIGTERM as-is since they exist on Windows
    
    replacements = [
        ('signal.SIGHUP', "getattr(signal, 'SIGHUP', signal.SIGTERM)"),
        ('signal.SIGCONT', "getattr(signal, 'SIGCONT', signal.SIGTERM)"),
        ('signal.SIGTSTP', "getattr(signal, 'SIGTSTP', signal.SIGTERM)"),
    ]
    
    patched = content
    for old, new in replacements:
        if old in patched and new not in patched:
            patched = patched.replace(old, new)
            print(f"Replaced: {old} -> {new}")
    
    if patched != content:
        with open(events_file, 'w', encoding='utf-8') as f:
            f.write(patched)
        print("\nPatch applied successfully!")
        print("You can now run: crewai run")
        return True
    else:
        print("No changes were needed or patterns not found.")
        return False


if __name__ == '__main__':
    success = patch_crewai()
    sys.exit(0 if success else 1)
