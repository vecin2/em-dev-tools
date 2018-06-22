from jinja2 import Environment, FileSystemLoader, select_autoescape, meta, Template
import shutil

env = Environment(
            loader=FileSystemLoader('/home/dgarcia/dev/python/em_dev_tools/repository/sql-template-engine/templates_old'),
            autoescape=select_autoescape(['html', 'xml'])
                )
template = env.get_template('add-verb.html')
print template.render(verb_id='inlineView')
template_source = env.loader.get_source(env, 'add-verb.html')[0]

def test_render_simple_template():
    template = Template('Hello {{ name }}!')
    assert "Hello John Doe!" == template.render(name='John Doe')

def test_list_token_names():
    env = Environment()
    ast = env.parse('Hello {{ name }}!')
    template_vars = meta.find_undeclared_variables(ast)
    assert "name" == list(template_vars)[0]

def test_it_does_not_list_token_if_value_set_within_temmplate():
    env = Environment()
    source ='{% set other_name = name %}Hello {{ name }}!, how are you {{ other_name }}'
    template = env.from_string(source)
    ast = env.parse(source)
    template_vars = meta.find_undeclared_variables(ast)
    assert "name" == next(iter(template_vars))
    assert "Hello David!, how are you David" == template.render(name='David')

def test_or_strucuture():
    env = Environment()
    source ='''Hello {{name or 'Pedro'}}!'''
    template = env.from_string(source)
    ast = env.parse(source)
    template_vars = meta.find_undeclared_variables(ast)
    assert "name" == next(iter(template_vars))
    assert "Hello Pedro!" == template.render()
