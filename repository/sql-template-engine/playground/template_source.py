from jinja2 import nodes
class TemplateSource(object):
    def __init__(self,ast):
        self.ast =ast
    def get_default_value(self, name):
        var_node = self.get_node_by_name(name)
        default_value=""
        if var_node:
            default_value = self.get_node_default_value(var_node)
        return default_value

    def get_value_description(self, name):
        var_node = self.get_node_by_name(name)
        default_value=""
        if var_node:
            default_value = self.get_node_value_description(var_node)
        return default_value

    def get_node_by_name(self,name):
        var_node = None
        for node in self.ast.body[0].nodes:
            if hasattr(node, "node"):
                if node.node.name == name:
                    var_node=node;
        return var_node

    def get_node_default_value(self,filter_node):
        if isinstance(filter_node, nodes.Filter) \
                & (filter_node.name == "default"):
                    return filter_node.args[0].value
        return ""

    def get_node_value_description(self,filter_node):
        if isinstance(filter_node, nodes.Filter) \
                & (filter_node.name == "description"):
                    return filter_node.args[0].value
        return ""