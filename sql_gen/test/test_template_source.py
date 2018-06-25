from jinja2 import Environment, meta, Template, nodes
from sql_gen.template_source import TemplateSource
import pytest
import sys

@pytest.fixture
def env():
    return  Environment()
    

def test_get_default_value(env):
    template = Template("Hello {{ name | default ('Mundo') }}!")
    ast = env.parse("Hello {{ name | default ('Mundo') }}!")

    template_source = TemplateSource(ast)

    assert "Mundo" == str(template_source.get_default_value("name"))

def description(value, description):
    return value

def test_get_description_value(env):
    env.filters['description']=description
    ast = env.parse("Hello {{ name | description ('Mundo') }}!")
    body_string="Output(nodes=[TemplateData(data=u'Hello '), "+ \
                              "Filter(node=Name(name='name', ctx='load'), "+\
                                     "name='default', "+\
                                     "args=[Const(value=u'Mundo')], "+\
                                     "kwargs=[], "+\
                                     "dyn_args=None, "+\
                                     "dyn_kwargs=None"+\
                                     "), "+\
                              "TemplateData(data=u'!')])"

    template_source = TemplateSource(ast)
    assert "Mundo" == str(template_source.get_description("name"))

