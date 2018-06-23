class TemplateSource():

def get_default_value(ast, name):
    var_node = get_node_by_name(ast,"name")
    default_value=""
    if var_node:
        default_value = get_node_default_value(var_node)
    return default_value

def get_node_by_name(ast,name):
    for node in ast.body[0].nodes:
        if hasattr(node, "node"):
            if node.node.name == name:
                var_node=node;
    return var_node

def get_node_default_value(filter_node):
    if isinstance(filter_node, nodes.Filter) \
       & (filter_node.name == "default"):
            return filter_node.args[0].value
    return ""
