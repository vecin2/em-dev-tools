from jinja2 import Environment, meta, Template, nodes
from sql_gen.sql_gen.template_source import TemplateSource
from sql_gen.sql_gen.filter_loader import load_filters
from anytree import Node
import pytest

@pytest.fixture
def env():
    env =  Environment()
    load_filters(env)
    return env
    
def test_anytree_node(env):
    ast = env.parse("Hello {{ name | default ('Mundo') | description ('World in english') }}!")
    filter_node =ast.body[0].nodes[1]
    assert "description" ==filter_node.name

    description_node = Node("description")
    nameNode = Node("name", parent=description_node, value=filter_node)

    assert "name"== description_node.children[0].name
    assert "description"== description_node.children[0].value.name

def test_traverse_template_nodes(env):
    ast = env.parse("Hello {{ prename }} {{ name | default ('Mundo') | description ('World in english') }}!")
    template_source = TemplateSource(ast)
    root_node = template_source.get_root_node()
    assert "Name(name='prename', ctx='load')" == str(root_node.children[0].value)
    assert "Filter(node=Filter(node=Name(name='name', ctx='load'), "+\
                               "name='default', "+\
                               "args=[Const(value=u'Mundo')], "+\
                               "kwargs=[], "+\
                               "dyn_args=None, "+\
                               "dyn_kwargs=None), "+\
                   "name='description', "+\
                   "args=[Const(value=u'World in english')], "+\
                   "kwargs=[], "+\
                   "dyn_args=None, "+\
                   "dyn_kwargs=None)" == str(root_node.children[1].value)
    assert "Filter(node=Name(name='name', ctx='load'), "+\
                  "name='default', "+\
                  "args=[Const(value=u'Mundo')], "+\
                  "kwargs=[], "+\
                  "dyn_args=None, "+\
                  "dyn_kwargs=None)" == str(root_node.children[1].children[0].value)
    assert "Name(name='name', ctx='load')" == str(root_node.children[1].children[0].children[0].value)


    
