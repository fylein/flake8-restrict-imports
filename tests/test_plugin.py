import ast
import os

import pytest
from restrict_imports.checker import Plugin


class TestPlugin:
    file_name: str = "restrict_imports"
    flake8_file_path: str = ".flake8"

    def test_when_allowed_imports_config_is_not_present(self):
        with open(self.flake8_file_path, 'w') as file:
            file.write(
                """
                [flake8]
                denied_imports_config={'plugin': ['tests'], 'tests': ['plugin']}
                """
            )
        import_node = ast.Import(names=[ast.alias(name='abcd', asname=None)], lineno=1, col_offset=1)
        tree = ast.Module(body=[import_node])
        plugin = Plugin(tree=tree, filename=self.file_name)
        with pytest.raises(ValueError):
            next(plugin.run())

        os.remove(self.flake8_file_path)

    def test_when_denied_imports_config_is_not_present(self):
        with open(self.flake8_file_path, 'w') as file:
            file.write(
                """
                [flake8]
                allowed_imports_config={'plugin': ['tests'], 'tests': ['plugin']}
                """
            )
        import_node = ast.Import(names=[ast.alias(name='abcd', asname=None)], lineno=1, col_offset=1)
        tree = ast.Module(body=[import_node])
        plugin = Plugin(tree=tree, filename=self.file_name)
        with pytest.raises(ValueError):
            next(plugin.run())

        os.remove(self.flake8_file_path)

    def test_when_correct_import_is_present(self):
        with open(self.flake8_file_path, 'w') as file:
            file.write(
                """
                [flake8]
                denied_imports_config={'plugin': ['tests'], 'tests': ['plugin']}
                allowed_imports_config={}
                """
            )

        import_node = ast.Import(names=[ast.alias(name='abcd', asname=None)], lineno=1, col_offset=1)
        tree = ast.Module(body=[import_node])
        plugin = Plugin(tree=tree, filename=self.file_name)
        with pytest.raises(StopIteration):
            next(plugin.run())
        
        os.remove(self.flake8_file_path)

    def test_when_denied_import_is_present(self):
        with open(self.flake8_file_path, 'w') as file:
            file.write(
                """
                [flake8]
                denied_imports_config={'plugin': ['tests'], 'tests': ['plugin']}
                allowed_imports_config={}
                """
            )

        import_node = ast.Import(names=[ast.alias(name='tests', asname=None)], lineno=1, col_offset=1)
        tree = ast.Module(body=[import_node])
        plugin = Plugin(tree=tree, filename=self.file_name)
        for lineno, col_offset, error_message, instance in plugin.run():
            assert error_message == "PRI001 cannot import tests in plugin module"
        
        os.remove(self.flake8_file_path)
