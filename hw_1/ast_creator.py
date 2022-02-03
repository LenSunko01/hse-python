import ast
import networkx as nx
import inspect
import fibonacci


class ASTCreator:
    def __init__(self, unparsed):
        ast_parsed = ast.parse(unparsed)
        self.graph = nx.Graph()
        self._last_node = 0
        self._build(ast_parsed)

    def _add_edge_if_ast(self, parent, child):
        if isinstance(child, ast.AST):
            self.graph.add_edge(parent, self._build(child))

    def _build(self, node) -> int:
        current_node = self._last_node
        label = node.__class__.__name__
        if isinstance(node, ast.Constant):
            label = f"Const = {node.value}"
        elif isinstance(node, ast.arg):
            label = f"Argument = {node.arg}"
        elif isinstance(node, ast.Sub):
            label = "Minus"
        elif isinstance(node, ast.Add):
            label = "Plus"
        elif isinstance(node, ast.FunctionDef):
            label = f"Function {node.name}"
        elif isinstance(node, ast.Name):
            label = f"Name = {node.id}"
        elif isinstance(node, ast.Attribute):
            label = f"Attribute = {node.attr}"
        self.graph.add_node(current_node, label = label)
        self._last_node += 1

        for _, v in ast.iter_fields(node):
            if isinstance(v, list):
                for i in v:
                    self._add_edge_if_ast(current_node, i)
            else:
                self._add_edge_if_ast(current_node, v)
        return current_node


if __name__ == "__main__":
    ast_object = ast.parse(inspect.getsource(fibonacci))
    creator = ASTCreator(ast_object)
    tree = creator.graph
    pydot_tree = nx.drawing.nx_pydot.to_pydot(tree)
    pydot_tree.write_png('./artifacts/ast.png')
