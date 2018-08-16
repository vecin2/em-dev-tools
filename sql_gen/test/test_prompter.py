from jinja2 import Environment, meta, Template, nodes
from sql_gen.sql_gen.template_source import TemplateSource
from sql_gen.sql_gen.prompter import Prompter
from sql_gen.sql_gen.filters import *
import pytest

@pytest.fixture
def env():
    env =  Environment()
    return env

def test_get_promts(env):
    ast = env.parse("Hello {{ name | default ('Mundo') }}!")
    prompter = Prompter(TemplateSource(ast))
    prompts = prompter.get_prompts()
    assert 1 == len(prompts)
    prompt = prompts[0]
    assert "name (default is Mundo): " == prompt.get_diplay_text()
    
