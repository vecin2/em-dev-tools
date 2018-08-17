from jinja2 import Environment, meta, Template, nodes
import pytest
import sys
from anytree import Node
from sql_gen.sql_gen.filter_loader import load_filters
import os

env = Environment()
load_filters(env)

def test_list_variable_names():
    ast = env.parse('Hello {{ name }}!')
    template_vars = meta.find_undeclared_variables(ast)
    assert "name" == list(template_vars)[0]

def test_fields():
    ast = env.parse('Hello {{ name }}!')
    #Template(body=[Output(nodes=[TemplateData(data=u'Hello '), Name(name='name', ctx='load'), TemplateData(data=u'!')])])
    fields=""
    for field in ast.fields:
        fields = fields + field
    assert "body" == fields

def test_template_body_structure():
    ast = env.parse('Hello {{ name }}!')
    for field, value in ast.iter_fields():
        assert "body" == field
        assert "[Output(nodes=[TemplateData(data=u'Hello '), Name(name='name', ctx='load'), TemplateData(data=u'!')])]" == str(value)
        assert  "Hello " == value[0].nodes[0].data
        assert  "name" == value[0].nodes[1].name
        assert  "!" == value[0].nodes[2].data


def test_get_description_value():
    ast = env.parse("Hello {{ name | default ('Mundo') }}!")
    body_string="Output(nodes=[TemplateData(data=u'Hello '), "+ \
                              "Filter(node=Name(name='name', ctx='load'), "+\
                                     "name='default', "+\
                                     "args=[Const(value=u'Mundo')], "+\
                                     "kwargs=[], "+\
                                     "dyn_args=None, "+\
                                     "dyn_kwargs=None"+\
                                     "), "+\
                              "TemplateData(data=u'!')])"
    assert body_string ==str(ast.body[0])

def test_pipe_default_descripion_filters():
    ast = env.parse("Hello {{ name | default ('Mundo') | description ('World in english') }}!")
    body_string="Output(nodes=[TemplateData(data=u'Hello '), "+ \
                              "Filter(node=Filter(" +\
                                        "node=Name(name='name', ctx='load'), "+\
                                        "name='default', "+\
                                        "args=[Const(value=u'Mundo')], "+\
                                        "kwargs=[], "+\
                                        "dyn_args=None, "+\
                                        "dyn_kwargs=None"+\
                                        "), "+\
                                      "name='description', "+\
                                      "args=[Const(value=u'World in english')], "+\
                                      "kwargs=[], dyn_args=None, "+\
                                      "dyn_kwargs=None"+\
                                      "), "+\
                              "TemplateData(data=u'!')])"
    

    assert body_string ==str(ast.body[0])

def test_anytree_node():
    ast = env.parse("Hello {{ name | default ('Mundo') | description ('World in english') }}!")
    filter_node =ast.body[0].nodes[1]
    assert "description" ==filter_node.name

    description_node = Node("description")
    nameNode = Node("name", parent=description_node, value=filter_node)

    assert "name"== description_node.children[0].name
    assert "description"== description_node.children[0].value.name


