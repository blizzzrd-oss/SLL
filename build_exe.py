"""
Build script for creating SLL executable with embedded resources.
This script creates a PyInstaller spec file and builds the executable.
"""

import os
import subprocess
import sys
from pathlib import Path

def create_spec_file():
    """Create an improved PyInstaller spec file."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

# Get absolute paths
project_root = Path(__file__).parent.absolute()
resources_path = project_root / "resources"

# Collect all resource files recursively
datas = []
if resources_path.exists():
    for root, dirs, files in os.walk(resources_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Calculate relative path from resources directory
            rel_path = os.path.relpath(file_path, project_root)
            # Add to datas with proper destination
            datas.append((file_path, os.path.dirname(rel_path)))

# Add settings file if it exists
settings_file = project_root / "settings.json"
if settings_file.exists():
    datas.append((str(settings_file), "."))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'pygame',
        'pygame.mixer',
        'pygame.font',
        'pygame.image',
        'pygame.transform',
        'pygame.math',
        'pygame.time',
        'pygame.display',
        'pygame.event',
        'pygame.key',
        'pygame.mouse',
        'pygame.rect',
        'pygame.surface',
        'json',
        'os',
        'sys',
        'math',
        'random',
        'collections',
        'datetime',
        'inspect'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2'
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SLL',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want console for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add path to .ico file if you have one: 'resources/icon.ico'
)
'''
    
    with open('SLL.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Created SLL.spec file")

def check_dependencies():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} is installed")
        return True
    except ImportError:
        print("❌ PyInstaller is not installed")
        print("Install it with: pip install pyinstaller")
        return False

def build_executable():
    """Build the executable using PyInstaller."""
    if not check_dependencies():
        return False
    
    print("🔨 Creating spec file...")
    create_spec_file()
    
    print("🔨 Building executable...")
    try:
        # Clean previous builds
        if os.path.exists('build'):
            print("🧹 Cleaning build directory...")
            subprocess.run(['rmdir', '/s', '/q', 'build'], shell=True, check=False)
        
        if os.path.exists('dist'):
            print("🧹 Cleaning dist directory...")
            subprocess.run(['rmdir', '/s', '/q', 'dist'], shell=True, check=False)
        
        # Build the executable
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--noconfirm',
            'SLL.spec'
        ], check=True, capture_output=True, text=True)
        
        print("✅ Build completed successfully!")
        print(f"📁 Executable location: {os.path.abspath('dist/SLL.exe')}")
        
        # Check file size
        exe_path = Path('dist/SLL.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📊 Executable size: {size_mb:.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with error: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

if __name__ == "__main__":
    print("🚀 Building SLL executable with embedded resources...")
    if build_executable():
        print("🎉 Build completed! You can now run dist/SLL.exe")
    else:
        print("💥 Build failed!")
        sys.exit(1)
