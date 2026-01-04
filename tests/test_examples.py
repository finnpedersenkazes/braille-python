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
        'example02',
        'example02a',
        'example02b',
        'example02c',
        'example04',
        'example05',
        'example06'
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
    """Test example01 (keyboard input with Elm architecture)"""

    def test_example01_structure(self):
        """Test example01 has correct structure"""
        import example01
        assert hasattr(example01, 'main')

    def test_example01_elm_architecture(self):
        """Test example01 has Elm architecture"""
        import example01
        assert hasattr(example01, 'init')
        assert hasattr(example01, 'view')
        assert hasattr(example01, 'update')


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
        import example04
        assert hasattr(example04, 'main')
        assert hasattr(example04, 'init')
        assert hasattr(example04, 'view')
        assert hasattr(example04, 'updateByKey')
        assert hasattr(example04, 'updateByTime')


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


class TestExample06:
    """Test example06 (character identification game)"""

    def test_example06_structure(self):
        """Test example06 has correct structure"""
        import example06
        assert hasattr(example06, 'main')

    def test_example06_elm_architecture(self):
        """Verify example06 uses Elm architecture"""
        import example06
        
        # Check for Elm architecture components
        assert hasattr(example06, 'init')
        assert hasattr(example06, 'view')
        assert hasattr(example06, 'update_by_key')
        assert hasattr(example06, 'update_by_game_start')
        assert hasattr(example06, 'update_by_new_challenge')
        
        # Check these are callable
        assert callable(example06.init)
        assert callable(example06.view)
        assert callable(example06.update_by_key)
        assert callable(example06.update_by_game_start)


class TestExampleSyntax:
    """Test that all examples have valid Python syntax"""

    def test_example_files_compile(self):
        """Test that all example files can be compiled"""
        import py_compile
        examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
        
        example_files = [
            'example01.py',
            'example02.py', 'example02a.py', 'example02b.py', 'example02c.py',
            'example04.py', 'example05.py', 'example06.py'
        ]
        
        for filename in example_files:
            filepath = os.path.join(examples_dir, filename)
            try:
                py_compile.compile(filepath, doraise=True)
            except py_compile.PyCompileError as e:
                pytest.fail(f"{filename} has syntax errors: {e}")
