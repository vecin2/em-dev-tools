from jinja2 import Environment, meta, Template, nodes
from template_source import TemplateSource
import pytest

env = Environment()
def test_list_token_names():
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

def test_extract_files_from_source():
    ast = env.parse('Hello {{ name }}!')
    for field, value in ast.iter_fields():
        assert "body" == field
        assert "[Output(nodes=[TemplateData(data=u'Hello '), Name(name='name', ctx='load'), TemplateData(data=u'!')])]" == str(value)
        assert  "Hello " == value[0].nodes[0].data
        assert  "name" == value[0].nodes[1].name
        assert  "!" == value[0].nodes[2].data

def test_print_var_name():
    template = Template("Hello {{ name | default ('Mundo') }}!")
    assert "Hello Mundo!" == template.render()

    ast = env.parse("Hello {{ name | default ('Mundo') }}!")
    field, value = next(ast.iter_fields())
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
    assert "Mundo" == str(template_source.get_default_value("name"))



    
