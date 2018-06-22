import os, shutil

def test_list_token_names():
    env = Environment()
    ast = env.parse('Hello {{ name }}!')
    template_vars = meta.find_undeclared_variables(ast)
    assert "name" == list(template_vars)[0]

    
