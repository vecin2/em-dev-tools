from jinja2 import Environment, meta, Template, nodes
#from sql_gen.sql_gen.filter_loader import loader_filters
from sql_gen.sql_gen.template_source import TemplateSource
from sql_gen.sql_gen.prompter import Prompter
import pytest

@pytest.fixture
def env():
    env =  Environment()
    load_filters(env)
    return env

def build_prompter(ast):
    return Prompter(TemplateSource(ast))
    
def test_prompt_default(env):
    ast = env.parse("Hello {{ name | default ('Mundo') }}!")
    prompter = build_prompter(ast)

    prompts = prompter.get_prompts()

    assert 1 == len(prompts)
    assert_display_text("name (default is Mundo): ", prompts[0])

def test_prompt_description(env):
    ast = env.parse("Hello {{ name | description ('customer name') }}!")
    prompter = build_prompter(ast)

    prompts = prompter.get_prompts()

    assert 1 == len(prompts)
    assert_display_text("customer name", prompts[0])


def assert_display_text(expected_text, prompt):
    assert expected_text == prompt.get_diplay_text()
    
