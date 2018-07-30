from jinja2 import Environment, meta, Template, nodes
from sql_gen.sql_gen.template_source import TemplateSource
from sql_gen.sql_gen.filters import *
import pytest

@pytest.fixture
def env():
    env =  Environment()
    env.filters['description']=description
    return env
    

def test_get_default_value(env):
    ast = env.parse("Hello {{ name | default ('Mundo') }}!")
    template_source = TemplateSource(ast)

    assert "Mundo" == str(template_source.get_default_value("name"))


def test_get_description_value(env):
    ast = env.parse("Hello {{ name | description ('Mundo') }}!")
    template_source = TemplateSource(ast)

    assert "Mundo" == str(template_source.get_description("name"))

def test_get_description_value_when_multiple_vars(env):
    ast = env.parse("Hello {{ prename }} {{ name | description ('Mundo') }}!")
    template_source = TemplateSource(ast)

    assert "Mundo" == str(template_source.get_description("name"))

def test_pipe_default_descripion_filters(env):
    ast = env.parse("Hello {{ name | default ('Mundo') | description ('World in english') }}!")
    template_source = TemplateSource(ast)
    assert "Mundo" ==str(template_source.get_default_value("name"))
    assert "World in english" == str(template_source.get_description("name"))

def test_pipe_default_descripion_filters_with_multiple_vars(env):
    ast = env.parse("Hello {{ prename }} {{ name | default ('Mundo') | description ('World in english') }}!")
    template_source = TemplateSource(ast)
    assert "Mundo" ==str(template_source.get_default_value("name"))
    assert "World in english" == str(template_source.get_description("name"))

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


