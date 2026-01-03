"""Integration tests for the braille-python development platform"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src and examples to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'examples'))


class TestDevelopmentPlatform(unittest.TestCase):
    """Test the overall development platform structure"""

    def test_src_directory_structure(self):
        """Test that src directory has expected files"""
        src_dir = os.path.join(os.path.dirname(__file__), '..', 'src')
        
        expected_files = ['library.py', 'model.py', 'update.py', 'view.py', 'main.py']
        for filename in expected_files:
            filepath = os.path.join(src_dir, filename)
            self.assertTrue(
                os.path.exists(filepath),
                f"{filename} should exist in src directory"
            )

    def test_examples_directory_structure(self):
        """Test that examples directory has expected files"""
        examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
        
        expected_files = [
            'example01.py',
            'example02.py', 'example02a.py', 'example02b.py', 'example02c.py',
            'example04.py', 'example05.py', 'example06.py'
        ]
        for filename in expected_files:
            filepath = os.path.join(examples_dir, filename)
            self.assertTrue(
                os.path.exists(filepath),
                f"{filename} should exist in examples directory"
            )

    def test_all_modules_import_cleanly(self):
        """Test that all src modules can be imported"""
        modules = ['library', 'model', 'update', 'view', 'main']
        
        for module_name in modules:
            with self.subTest(module=module_name):
                module = __import__(module_name)
                self.assertIsNotNone(module)


class TestElmArchitecture(unittest.TestCase):
    """Test Elm architecture implementation"""

    def test_example05_elm_architecture(self):
        """Test example05 implements full Elm architecture"""
        import example05
        
        # Check for init, update, view pattern
        self.assertTrue(hasattr(example05, 'init'))
        self.assertTrue(hasattr(example05, 'updateByTime'))
        self.assertTrue(hasattr(example05, 'updateByKey'))
        self.assertTrue(hasattr(example05, 'view'))
        
        # Test init returns a dictionary (model)
        mock_brl = Mock()
        mock_brl.displaySize = (20, 1)
        model = example05.init(mock_brl)
        self.assertIsInstance(model, dict)
        
        # Model should have expected keys
        expected_keys = ['cursorPos', 'obstaclePos', 'points', 'collision', 'stop', 'counter', 'displayWidth', 'message']
        for key in expected_keys:
            self.assertIn(key, model, f"Model should have '{key}' key")

    def test_example04_elm_architecture(self):
        """Test example04 implements Elm architecture"""
        import example04
        
        # Check for init, update, view pattern
        self.assertTrue(hasattr(example04, 'init'))
        self.assertTrue(hasattr(example04, 'updateByKey'))
        self.assertTrue(hasattr(example04, 'view'))
        
        # Test init returns a model
        mock_brl = Mock()
        mock_brl.displaySize = (20, 1)
        model = example04.init(mock_brl)
        self.assertIsInstance(model, dict)


class TestLauncherIntegration(unittest.TestCase):
    """Test launcher integrates with examples"""

    @patch('sys.argv', ['main.py', '05'])
    @patch('example05.main')
    def test_launcher_runs_example05(self, mock_example_main):
        """Test launcher can run example05"""
        import main
        
        # Run main (it will import example05 and call its main)
        with patch('builtins.print'):
            main.main()
        
        # Verify example05.main was called
        mock_example_main.assert_called_once()


class TestConsistency(unittest.TestCase):
    """Test consistency across examples"""

    def test_all_examples_use_consistent_shebang(self):
        """Test that all examples have shebang lines"""
        examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
        example_files = [
            'example01.py',
            'example02.py', 'example02a.py', 'example02b.py', 'example02c.py',
            'example04.py', 'example05.py', 'example06.py'
        ]
        
        for filename in example_files:
            filepath = os.path.join(examples_dir, filename)
            with self.subTest(file=filename):
                with open(filepath, 'r') as f:
                    first_line = f.readline()
                    self.assertTrue(
                        first_line.startswith('#!'),
                        f"{filename} should have a shebang line"
                    )

    def test_all_examples_have_consistent_main_pattern(self):
        """Test that all examples use if __name__ == '__main__' pattern"""
        examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
        example_files = [
            'example01.py',
            'example02.py', 'example02a.py', 'example02b.py', 'example02c.py',
            'example04.py', 'example05.py', 'example06.py'
        ]
        
        for filename in example_files:
            filepath = os.path.join(examples_dir, filename)
            with self.subTest(file=filename):
                with open(filepath, 'r') as f:
                    content = f.read()
                    self.assertIn(
                        'if __name__ == "__main__":',
                        content,
                        f"{filename} should have if __name__ == '__main__' guard"
                    )
                    self.assertIn(
                        'def main():',
                        content,
                        f"{filename} should have def main() function"
                    )


if __name__ == '__main__':
    unittest.main()
