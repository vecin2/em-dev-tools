from jinja2 import nodes,meta
from anytree import Node
#from sql_gen.filters.default import DefaultFilter

class DefaultFilter(object):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(self, prompt_text):
        default_unicode= self.filter.args[0].value
        if default_unicode:
            default_value= default_unicode.encode('ascii','ignore')
            prompt_text = prompt_text + " (default is "+default_value+")"
        return prompt_text

class DescriptionFilter(object):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(display_text):
        description_unicode= self.filter.args[0].value
        return default_unicode.encode('ascii','ignore')

class TemplateNode(object):
    def __init__(self, ast):
        self.ast_nodes =ast.body[0].nodes
        self.root=""
        self.root = self.get_root_node()

    def get_root_node(self):
        if self.root:
            return self.root
        else:
            self.root = Node("templateRoot")
            for node in self.ast_nodes:
                   self.add_children_nodes(node,self.root)
            return self.root

    def add_children_nodes(self,node,parent):
        node_value = node
        if node_value:
            if (hasattr(node_value, "name")):
                current_node = Node(node_value.name, parent, value=node)
                if hasattr(node_value, "node"):
                     self.add_children_nodes(node_value.node,current_node)

        return

    def get_filter_arg_value_by_node_name(self,filter_name,node_name):
        tree_node = self.get_tree_node_by_name(self.root, node_name)
        if tree_node:
            parent_node =tree_node.parent
            while parent_node:
                if hasattr(parent_node, "value"):
                    parent_filter = parent_node.value
                    if parent_filter.name == filter_name:
                        return self.get_arg_value(parent_filter)

                parent_node = parent_node.parent
                
        return ""

    def get_tree_node_by_name(self,parent,name):
        if not parent.children:
            return None
        for node in parent.children:
            if(node.name == name):
                return node
            else:
                child = self.get_tree_node_by_name(node, name)
                if child:
                    return child
        return

    def get_arg_value(self,filter_node):
        if isinstance(filter_node, nodes.Filter):
                    return filter_node.args[0].value
        return ""

    def get_filters(self, node_name):
        node = self.get_tree_node_by_name(self.root,node_name)
        result=[]
        for current_node in node.ancestors:
            if (hasattr(current_node, "value")) and\
                isinstance(current_node.value, nodes.Filter):
                    result.append(current_node.value)

        return result

class TemplateSource(object):
    def __init__(self,ast):
        self.ast =ast
        self.ast_nodes =self.ast.body[0].nodes
        self.root=""
        self.root = self.get_root_node()
        self.template_name=""
       # self.root_node = TemplateNode(self.ast)

    def get_template(self):
        return self.template;

    def find_undeclared_variables(self):
        return meta.find_undeclared_variables(self.ast)

    def get_root_node(self):
        if self.root:
            return self.root
        else:
            self.root = Node("templateRoot")
            for node in self.ast_nodes:
                   self.add_children_nodes(node,self.root)
            return self.root

    def add_children_nodes(self,node,parent):
        node_value = node
        if node_value:
            if (hasattr(node_value, "name")):
                current_node = Node(node_value.name, parent, value=node)
                if hasattr(node_value, "node"):
                     self.add_children_nodes(node_value.node,current_node)

        return

    def get_default_value(self, name):
        return self.get_filter_arg_value_by_node_name("default", name)

    def get_description(self, name):
        return self.get_filter_arg_value_by_node_name("description", name)

    def get_filter_arg_value_by_node_name(self,filter_name,node_name):
        tree_node = self.get_tree_node_by_name(self.root, node_name)
        if tree_node:
            parent_node =tree_node.parent
            while parent_node:
                if hasattr(parent_node, "value"):
                    parent_filter = parent_node.value
                    if parent_filter.name == filter_name:
                        return self.get_arg_value(parent_filter)

                parent_node = parent_node.parent
                
        return ""

    def get_tree_node_by_name(self,parent,name):
        if not parent.children:
            return None
        for node in parent.children:
            if(node.name == name):
                return node
            else:
                child = self.get_tree_node_by_name(node, name)
                if child:
                    return child
        return

    def get_arg_value(self,filter_node):
        if isinstance(filter_node, nodes.Filter):
                    return filter_node.args[0].value
        return ""

    def get_filters(self, node_name):
        node = self.get_tree_node_by_name(self.root,node_name)
        result=[]
        for current_node in node.ancestors:
            if (hasattr(current_node, "value")) and\
                isinstance(current_node.value, nodes.Filter):
                    result.append(DefaultFilter(current_node.value))

        return result
