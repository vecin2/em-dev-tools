import pytest
from jinja2 import Environment
from sql_gen.sql_gen.prompter import Prompter
from sql_gen.sql_gen.template_source import TemplateSource
from sql_gen.sql_gen.environment_selection import TemplateSelector, EMTemplatesEnv

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
    assert_display_text("name (default is Mundo)", prompts[0])

def assert_display_text(expected_text, prompt):
    assert expected_text+ ": " == prompt.get_diplay_text()
