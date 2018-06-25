from jinja2 import Environment, meta, Template, nodes
from sql_gen.sql_gen.template_source import TemplateSource
from sql_gen.sql_gen.filters import *
import pytest

@pytest.fixture
def env():
    return  Environment()
    

def test_get_default_value(env):
    template = Template("Hello {{ name | default ('Mundo') }}!")
    ast = env.parse("Hello {{ name | default ('Mundo') }}!")

    template_source = TemplateSource(ast)

    assert "Mundo" == str(template_source.get_default_value("name"))


def test_get_description_value(env):
    env.filters['description']=description
    ast = env.parse("Hello {{ name | description ('Mundo') }}!")
    template_source = TemplateSource(ast)
    assert "Mundo" == str(template_source.get_description("name"))

