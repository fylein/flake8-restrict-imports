import ast
import configparser
import enum
import json
import os

from typing import Dict, List, Tuple, Generator


class RestrictImportsErrorCodes(enum.Enum):
    RESTRICT_IMPORT = "PRI001"
    RESTRICT_IMPORT_FROM = "PRI002"


class Visitor(ast.NodeVisitor):
    options = None

    def __init__(self, current_module: str, current_filename: str, errors: List[Tuple[int, int, str]]) -> None:
        self.current_module = current_module
        self.current_filename = current_filename
        self.errors = errors


    @classmethod
    def load_imports_config(cls) -> Tuple[Dict, Dict]:
        config = configparser.ConfigParser()
        config.read('.flake8')
        denied_imports_config = config['flake8'].get('denied_imports_config', None)
        allowed_imports_config = config['flake8'].get('allowed_imports_config', None)

        if denied_imports_config is None:
            raise ValueError("Configuration 'denied_imports_config' is missing in the .flake8 file.")

        if allowed_imports_config is None:
            raise ValueError("Configuration 'allowed_imports_config' is missing in the .flake8 file.")

        denied_imports_config = denied_imports_config.replace("'", "\"")
        allowed_imports_config = allowed_imports_config.replace("'", "\"")
        
        denied_imports = json.loads(denied_imports_config)
        allowed_imports = json.loads(allowed_imports_config)

        return denied_imports, allowed_imports


    @classmethod
    def denied_import(cls, *, current_module: str, imported_module: str) -> bool:
        denied_imports, allowed_imports = cls.load_imports_config()

        for k, v in denied_imports.items():
            if current_module.startswith(k):  
                for v1 in v:
                    if imported_module.startswith(v1):
                        return True
    
        for k, v in allowed_imports.items():
            if current_module.startswith(k):
                for v1 in v:
                    if imported_module.startswith(v1):
                        return False


    def visit_Import(self, node: ast.Import) -> None:
        for n in node.names:
            if n.name and self.denied_import(current_module=self.current_module, imported_module=n.name):
                self.errors.append((node.lineno, node.col_offset, f'PRI001 cannot import {n.name} in {self.current_module} module'))

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module and self.denied_import(current_module=self.current_module, imported_module=node.module):
            self.errors.append((node.lineno, node.col_offset, f'PRI002 cannot import {node.module} in {self.current_module} module'))


class Plugin:
    """Restrict imports checker"""
    name = 'restrict_imports'
    version = '0.1.1'

    def __init__(self, tree: ast.AST, filename: str):
        self.tree = tree
        self.current_filename = filename
        path = os.path.splitext(filename)[0]
        mod_path = []
        while path:
            if os.path.exists(os.path.join(path, '.flake8')):
                break
            dir, name = os.path.split(path)
            mod_path.insert(0, name)
            path = dir
        self.current_module = '.'.join(mod_path)

    def run(self) -> Generator:
        errors: List[Tuple[int, int, str]] = []
        visitor = Visitor(current_module=self.current_module, current_filename=self.current_filename, errors=errors)
        visitor.visit(self.tree)
        for lineno, colno, msg in errors:
            yield lineno, colno, msg, type(self)
