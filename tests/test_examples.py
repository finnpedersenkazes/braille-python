"""Tests for example files"""
import sys
import os
import pytest

# Add examples to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'examples'))


class TestExampleStructure:
    """Test that all examples have consistent structure"""
    
    examples = [
        'example01',
        'example01a', 
        'example01b',
        'example02',
        'example02a',
        'example02b',
        'example02c',
        'example04a',
        'example05'
    ]
    
    @pytest.mark.parametrize("example_name", examples)
    def test_example_has_main_function(self, example_name):
        """Test that example has a main() function"""
        module = __import__(example_name)
        assert hasattr(module, 'main'), f"{example_name} should have a main() function"
        assert callable(module.main), f"{example_name}.main should be callable"
    
    @pytest.mark.parametrize("example_name", examples)
    def test_example_has_name_main_guard(self, example_name):
        """Test that example has if __name__ == '__main__' guard"""
        example_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'examples', 
            f'{example_name}.py'
        )
        with open(example_path, 'r') as f:
            content = f.read()
        assert 'if __name__ == "__main__"' in content, \
            f"{example_name} should have if __name__ == '__main__' guard"
    
    @pytest.mark.parametrize("example_name", examples)
    def test_example_imports_brlapi(self, example_name):
        """Test that example imports brlapi"""
        example_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'examples', 
            f'{example_name}.py'
        )
        with open(example_path, 'r') as f:
            content = f.read()
        assert 'import brlapi' in content, \
            f"{example_name} should import brlapi"


class TestExample01Series:
    """Test example01 series (keyboard input examples)"""

    def test_example01_structure(self):
        """Test example01 has correct structure"""
        import example01
        assert hasattr(example01, 'main')

    def test_example01a_structure(self):
        """Test example01a has correct structure"""
        import example01a
        assert hasattr(example01a, 'main')

    def test_example01b_elm_architecture(self):
        """Test example01b has Elm architecture"""
        import example01b
        assert hasattr(example01b, 'main')
        assert hasattr(example01b, 'init')
        assert hasattr(example01b, 'view')
        assert hasattr(example01b, 'update')


class TestExample02Series:
    """Test example02 series (display examples)"""

    def test_example02_structure(self):
        """Test example02 has correct structure"""
        import example02
        assert hasattr(example02, 'main')

    def test_example02a_structure(self):
        """Test example02a has correct structure"""
        import example02a
        assert hasattr(example02a, 'main')

    def test_example02b_structure(self):
        """Test example02b has correct structure"""
        import example02b
        assert hasattr(example02b, 'main')

    def test_example02c_structure(self):
        """Test example02c has correct structure"""
        import example02c
        assert hasattr(example02c, 'main')


class TestExample04Series:
    """Test example04 series (keyboard learning game)"""

    def test_example04a_elm_architecture(self):
        """Test example04a has Elm architecture"""
        import example04a
        assert hasattr(example04a, 'main')
        assert hasattr(example04a, 'init')
        assert hasattr(example04a, 'view')
        assert hasattr(example04a, 'updateByKey')
        assert hasattr(example04a, 'updateByTime')


class TestExample05:
    """Test example05 (obstacle jump game)"""

    def test_example05_structure(self):
        """Test example05 has correct structure"""
        import example05
        assert hasattr(example05, 'main')

    def test_example05_elm_architecture(self):
        """Verify example05 uses Elm architecture"""
        import example05
        
        # Check for Elm architecture components
        assert hasattr(example05, 'init')
        assert hasattr(example05, 'view')
        assert hasattr(example05, 'updateByTime')
        assert hasattr(example05, 'updateByKey')
        
        # Check these are callable
        assert callable(example05.init)
        assert callable(example05.view)
        assert callable(example05.updateByTime)
        assert callable(example05.updateByKey)


class TestExampleSyntax:
    """Test that all examples have valid Python syntax"""

    def test_example_files_compile(self):
        """Test that all example files can be compiled"""
        import py_compile
        examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
        
        example_files = [
            'example01.py', 'example01a.py', 'example01b.py',
            'example02.py', 'example02a.py', 'example02b.py', 'example02c.py',
            'example04a.py', 'example05.py'
        ]
        
        for filename in example_files:
            filepath = os.path.join(examples_dir, filename)
            try:
                py_compile.compile(filepath, doraise=True)
            except py_compile.PyCompileError as e:
                pytest.fail(f"{filename} has syntax errors: {e}")
