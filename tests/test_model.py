"""Tests for src/model.py module"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestModelModule(unittest.TestCase):
    """Test model module functionality"""

    def test_model_module_imports(self):
        """Test that model module can be imported"""
        import model
        self.assertIsNotNone(model)

    def test_model_has_printDiagnostics(self):
        """Test that model module has printDiagnostics function"""
        import model
        self.assertTrue(hasattr(model, 'printDiagnostics'))
        self.assertTrue(callable(model.printDiagnostics))

    @patch('model.printProperty')
    def test_printDiagnostics_calls_printProperty(self, mock_print_property):
        """Test that printDiagnostics calls printProperty for each field"""
        import model
        import brlapi
        
        # Create mock braille connection
        mock_brl = Mock()
        mock_brl.fileDescriptor = 5
        mock_brl.host = "localhost"
        mock_brl.auth = "keyfile"
        mock_brl.driverName = "test_driver"
        mock_brl.modelIdentifier = "test_model"
        mock_brl.displaySize = (20, 1)
        
        model.printDiagnostics(mock_brl)
        
        # Verify printProperty was called
        self.assertGreater(mock_print_property.call_count, 0)


class TestModelPatterns(unittest.TestCase):
    """Test model patterns and documentation"""

    def test_model_module_is_template(self):
        """Test that model module serves as template/documentation"""
        import model
        
        # Module should have docstring explaining its purpose
        self.assertIsNotNone(model.__doc__)
        self.assertIn("Elm", model.__doc__)


if __name__ == '__main__':
    unittest.main()
