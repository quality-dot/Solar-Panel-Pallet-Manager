#!/usr/bin/env python3
"""
Path Utilities - Handles path resolution for both development and packaged environments

This module provides utilities to correctly resolve paths whether the application
is running as a script or as a packaged executable.
"""

import sys
import os
from pathlib import Path
from typing import Optional


def is_packaged() -> bool:
    """
    Check if the application is running as a packaged executable.
    
    Returns:
        True if running as packaged executable (PyInstaller, py2app, etc.)
        False if running as a Python script
    """
    # PyInstaller sets sys.frozen to True
    if getattr(sys, 'frozen', False):
        return True
    
    # Check if running from a .app bundle (macOS)
    if sys.platform == 'darwin':
        if '.app/Contents' in sys.executable or '.app/Contents' in __file__:
            return True
    
    # Check if running from .exe (Windows)
    if sys.platform == 'win32':
        if sys.executable.endswith('.exe') and 'python' not in sys.executable.lower():
            return True
    
    return False


def get_base_dir() -> Path:
    """
    Get the base directory of the application.
    
    In development: Returns the project root directory
    In packaged: Returns a writable directory for data files
    
    For macOS apps in /Applications/, uses ~/Documents/Pallet Manager/
    For other locations, uses directory containing the app
    
    Returns:
        Path to the base directory
    """
    # Check for PyInstaller first (sys._MEIPASS is set during extraction)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # PyInstaller (Windows/Linux): executable is in dist/, base is executable's parent
        # For one-file builds, sys._MEIPASS is temp extraction dir (don't use)
        # For one-dir builds, sys._MEIPASS is the _internal dir (don't use)
        # We want the directory containing the executable
        return Path(sys.executable).parent
    
    # Check for py2app (macOS .app bundle)
    if getattr(sys, 'frozen', False) and sys.platform == 'darwin':
        # py2app: sys.executable points to executable inside .app/Contents/MacOS/
        exe_path = Path(sys.executable)
        if '.app/Contents' in str(exe_path):
            # Navigate up from .app/Contents/MacOS/executable to .app/../
            # Structure: /path/to/Pallet Manager.app/Contents/MacOS/pallet_builder_gui
            app_dir = exe_path
            while app_dir.name != 'Contents' and app_dir.parent != app_dir:
                app_dir = app_dir.parent
            if app_dir.name == 'Contents':
                # app_dir is Contents/, parent is .app/, parent.parent is base dir
                app_bundle_dir = app_dir.parent.parent  # .app/../
                
                # If app is in /Applications/, use user's Documents folder instead
                # (Applications folder is not writable)
                if str(app_bundle_dir) == '/Applications' or app_bundle_dir.parent.name == 'Applications':
                    # Use ~/Documents/Pallet Manager/ for data files
                    documents_dir = Path.home() / 'Documents' / 'Pallet Manager'
                    documents_dir.mkdir(parents=True, exist_ok=True)
                    return documents_dir
                
                # If app is in a writable location, use that directory
                # Check if we can write to the directory
                try:
                    test_file = app_bundle_dir / '.pallet_manager_test'
                    test_file.touch()
                    test_file.unlink()
                    # Directory is writable, use it
                    return app_bundle_dir
                except (PermissionError, OSError):
                    # Directory is not writable, use Documents instead
                    documents_dir = Path.home() / 'Documents' / 'Pallet Manager'
                    documents_dir.mkdir(parents=True, exist_ok=True)
                    return documents_dir
        
        # Fallback: if not in .app structure, use executable's parent
        return exe_path.parent
    
    # Check for other packaged formats
    if is_packaged():
        # Windows .exe or other formats
        return Path(sys.executable).parent
    
    # Development: return project root (parent of app directory)
    # This file is in app/, so parent.parent is project root
    return Path(__file__).parent.parent


def get_app_dir() -> Path:
    """
    Get the app directory (where Python modules are located).
    
    In development: Returns app/ directory
    In packaged: Returns the same as base_dir (executable directory)
    
    Returns:
        Path to the app directory
    """
    if is_packaged():
        # When packaged, app code is bundled with executable
        # Use base_dir as app_dir
        return get_base_dir()
    else:
        # Development: app/ directory
        return Path(__file__).parent


def resolve_project_path(relative_path: str) -> Path:
    """
    Resolve a path relative to the project root.
    
    Args:
        relative_path: Path relative to project root (e.g., "PALLETS/history.json")
    
    Returns:
        Absolute Path to the resolved location
    """
    base_dir = get_base_dir()
    return (base_dir / relative_path).resolve()


def get_resource_path(relative_path: str) -> Path:
    """
    Get path to a resource file (for bundled resources in packaged apps).
    
    Args:
        relative_path: Path relative to project root
    
    Returns:
        Path to the resource file
    """
    if is_packaged():
        # In packaged app, resources are in the same directory as executable
        # or in a _internal/ subdirectory (PyInstaller)
        base = get_base_dir()
        
        # Try direct path first
        direct_path = base / relative_path
        if direct_path.exists():
            return direct_path
        
        # Try _internal/ subdirectory (PyInstaller)
        internal_path = base / "_internal" / relative_path
        if internal_path.exists():
            return internal_path
        
        # Return direct path even if it doesn't exist (will be created)
        return direct_path
    else:
        # Development: use project root
        return resolve_project_path(relative_path)


# Common project paths (cached for performance)
_base_dir_cache: Optional[Path] = None
_app_dir_cache: Optional[Path] = None


def get_base_dir_cached() -> Path:
    """Get base directory with caching for performance"""
    global _base_dir_cache
    if _base_dir_cache is None:
        _base_dir_cache = get_base_dir()
    return _base_dir_cache


def get_app_dir_cached() -> Path:
    """Get app directory with caching for performance"""
    global _app_dir_cache
    if _app_dir_cache is None:
        _app_dir_cache = get_app_dir()
    return _app_dir_cache


