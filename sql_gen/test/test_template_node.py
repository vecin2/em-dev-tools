from jinja2 import Environment, meta, Template, nodes
from sql_gen.sql_gen.template_source import TemplateSource,TemplateNode
from sql_gen.sql_gen.filters import *
import pytest



@pytest.fixture
def env():
    env =  Environment()
    env.filters['description']=description
    return env
    

def test_get_filters(env):
    ast = env.parse("Hello {{ name | default ('Mundo') }}!")
    node = TemplateNode(ast)
    parents = node.get_filters("name")
    
    assert "default" == str(parents[0].name)

