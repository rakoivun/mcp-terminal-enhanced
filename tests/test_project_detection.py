#!/usr/bin/env python3
"""
Test project root detection functionality.

These tests verify that the enhanced MCP wrapper correctly detects
project root directories based on common project markers.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add src to path for importing the wrapper
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from terminal_controller_wrapper import get_project_root, PROJECT_MARKERS
except ImportError:
    print("Error: Could not import terminal_controller_wrapper")
    print("Make sure you're running tests from the project root directory")
    sys.exit(1)


class TestProjectDetection(unittest.TestCase):
    """Test cases for project root detection."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
    
    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_project_structure(self, structure):
        """
        Create a test project structure.
        
        Args:
            structure: Dict representing directory structure
        """
        def create_items(base_path, items):
            for name, content in items.items():
                item_path = os.path.join(base_path, name)
                if isinstance(content, dict):
                    # Directory
                    os.makedirs(item_path, exist_ok=True)
                    create_items(item_path, content)
                else:
                    # File
                    os.makedirs(os.path.dirname(item_path), exist_ok=True)
                    with open(item_path, 'w') as f:
                        f.write(content or '')
        
        create_items(self.temp_dir, structure)
    
    def test_git_repository_detection(self):
        """Test detection of Git repositories."""
        self.create_project_structure({
            'project': {
                '.git': {
                    'config': '[core]\nrepositoryformatversion = 0'
                },
                'src': {
                    'main.py': 'print("hello")'
                },
                'subdir': {
                    'module.py': 'import os'
                }
            }
        })
        
        project_root = os.path.join(self.temp_dir, 'project')
        subdir = os.path.join(project_root, 'subdir')
        
        # Test from project root
        detected = get_project_root(project_root)
        self.assertEqual(detected, project_root)
        
        # Test from subdirectory
        detected = get_project_root(subdir)
        self.assertEqual(detected, project_root)
    
    def test_nodejs_project_detection(self):
        """Test detection of Node.js projects."""
        self.create_project_structure({
            'webapp': {
                'package.json': '{"name": "test-app", "version": "1.0.0"}',
                'src': {
                    'index.js': 'console.log("hello");'
                },
                'node_modules': {
                    'express': {
                        'package.json': '{"name": "express"}'
                    }
                }
            }
        })
        
        project_root = os.path.join(self.temp_dir, 'webapp')
        src_dir = os.path.join(project_root, 'src')
        
        detected = get_project_root(src_dir)
        self.assertEqual(detected, project_root)
    
    def test_python_project_detection(self):
        """Test detection of Python projects."""
        # Test pyproject.toml
        self.create_project_structure({
            'python_app': {
                'pyproject.toml': '[build-system]\nrequires = ["setuptools"]',
                'src': {
                    'mypackage': {
                        '__init__.py': '',
                        'main.py': 'def main(): pass'
                    }
                },
                'tests': {
                    'test_main.py': 'import unittest'
                }
            }
        })
        
        project_root = os.path.join(self.temp_dir, 'python_app')
        tests_dir = os.path.join(project_root, 'tests')
        
        detected = get_project_root(tests_dir)
        self.assertEqual(detected, project_root)
        
        # Test setup.py
        self.create_project_structure({
            'legacy_python': {
                'setup.py': 'from setuptools import setup; setup()',
                'mypackage': {
                    '__init__.py': ''
                }
            }
        })
        
        legacy_root = os.path.join(self.temp_dir, 'legacy_python')
        detected = get_project_root(os.path.join(legacy_root, 'mypackage'))
        self.assertEqual(detected, legacy_root)
    
    def test_rust_project_detection(self):
        """Test detection of Rust projects."""
        self.create_project_structure({
            'rust_app': {
                'Cargo.toml': '[package]\nname = "rust_app"\nversion = "0.1.0"',
                'src': {
                    'main.rs': 'fn main() { println!("Hello, world!"); }'
                },
                'target': {
                    'debug': {}
                }
            }
        })
        
        project_root = os.path.join(self.temp_dir, 'rust_app')
        src_dir = os.path.join(project_root, 'src')
        
        detected = get_project_root(src_dir)
        self.assertEqual(detected, project_root)
    
    def test_go_project_detection(self):
        """Test detection of Go projects."""
        self.create_project_structure({
            'go_app': {
                'go.mod': 'module github.com/user/go_app\n\ngo 1.19',
                'main.go': 'package main\n\nfunc main() {}',
                'internal': {
                    'handler.go': 'package internal'
                }
            }
        })
        
        project_root = os.path.join(self.temp_dir, 'go_app')
        internal_dir = os.path.join(project_root, 'internal')
        
        detected = get_project_root(internal_dir)
        self.assertEqual(detected, project_root)
    
    def test_no_project_markers(self):
        """Test behavior when no project markers are found."""
        self.create_project_structure({
            'random_dir': {
                'file1.txt': 'content',
                'subdir': {
                    'file2.txt': 'content'
                }
            }
        })
        
        subdir = os.path.join(self.temp_dir, 'random_dir', 'subdir')
        
        # Should return the starting directory when no markers found
        detected = get_project_root(subdir)
        self.assertEqual(detected, subdir)
    
    def test_multiple_markers_priority(self):
        """Test that markers are detected in priority order."""
        self.create_project_structure({
            'complex_project': {
                '.git': {
                    'config': '[core]'
                },
                'package.json': '{"name": "test"}',
                'setup.py': 'from setuptools import setup',
                'src': {
                    'main.py': 'print("hello")'
                }
            }
        })
        
        project_root = os.path.join(self.temp_dir, 'complex_project')
        src_dir = os.path.join(project_root, 'src')
        
        # Should detect .git first (highest priority)
        detected = get_project_root(src_dir)
        self.assertEqual(detected, project_root)
    
    def test_nested_projects(self):
        """Test detection in nested project structures."""
        self.create_project_structure({
            'monorepo': {
                '.git': {
                    'config': '[core]'
                },
                'apps': {
                    'frontend': {
                        'package.json': '{"name": "frontend"}',
                        'src': {
                            'index.js': 'content'
                        }
                    },
                    'backend': {
                        'pyproject.toml': '[tool.poetry]',
                        'src': {
                            'main.py': 'content'
                        }
                    }
                }
            }
        })
        
        monorepo_root = os.path.join(self.temp_dir, 'monorepo')
        frontend_src = os.path.join(monorepo_root, 'apps', 'frontend', 'src')
        
        # Should find the monorepo root (.git has higher priority)
        detected = get_project_root(frontend_src)
        self.assertEqual(detected, monorepo_root)
    
    def test_marker_priority_order(self):
        """Test that PROJECT_MARKERS list is in correct priority order."""
        # .git should be first (highest priority)
        self.assertEqual(PROJECT_MARKERS[0], '.git')
        
        # Common project files should be early in the list
        high_priority_markers = ['.git', 'package.json', 'pyproject.toml', 'setup.py']
        for marker in high_priority_markers:
            self.assertIn(marker, PROJECT_MARKERS[:10])  # Should be in top 10


class TestEnvironmentSetup(unittest.TestCase):
    """Test environment setup functionality."""
    
    def test_project_markers_complete(self):
        """Test that PROJECT_MARKERS contains expected markers."""
        expected_markers = [
            '.git', 'package.json', 'pyproject.toml', 'setup.py',
            'Cargo.toml', 'go.mod', 'pom.xml', 'build.gradle',
            'composer.json', 'Gemfile', 'Makefile', 'CMakeLists.txt'
        ]
        
        for marker in expected_markers:
            self.assertIn(marker, PROJECT_MARKERS, 
                         f"Expected marker '{marker}' not found in PROJECT_MARKERS")
    
    def test_import_functionality(self):
        """Test that all required functions can be imported."""
        try:
            from terminal_controller_wrapper import (
                get_project_root, 
                detect_git_bash, 
                setup_environment,
                PROJECT_MARKERS
            )
        except ImportError as e:
            self.fail(f"Failed to import required functions: {e}")


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)