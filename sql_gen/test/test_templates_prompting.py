import pytest
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sql_gen.sql_gen.filter_loader import load_filters
from sql_gen.sql_gen.prompter import Prompter
from sql_gen.sql_gen.template_source import TemplateSource
import os
#from sql_gen.sql_gen.environment_selection import TemplateSelector
#from sql_gen.environment_selection import TemplateSelector, EMTemplatesEnv

    
def test_process_descriptor_prompts():
    expected_msgs=["repository_path",
                   "process_descriptor_name",
                   "config_id (default is NULL)",
                   "type_id (0=regular process, 2=action, 3=sla) (default is 0)"
                   ]
    template_name="add_process_descriptor.sql"

    assert_template_prompts_messages(expected_msgs,template_name)

def assert_template_prompts_messages(expected_msgs,template_name):
    env = get_env()
    source = env.loader.get_source(env,template_name)[0]
    prompter = Prompter(TemplateSource(env.parse(source)))
    prompts = prompter.get_prompts()

    assert_prompts(expected_msgs, prompts)

def get_env():
    templates_path =os.environ['SQL_TEMPLATES_PATH']
    env = Environment(
    loader=FileSystemLoader(templates_path),
            autoescape=select_autoescape(['html', 'xml']))
    load_filters(env)
    return env


def assert_prompts(expected_msgs, prompts):
    assert len(expected_msgs) == len(prompts)
    current_index =0
    for expected_msg in expected_msgs:
        assert_display_text(expected_msg, prompts[current_index])
        current_index = current_index +1

def assert_display_text(expected_text, prompt):
    assert expected_text+ ": " == prompt.get_diplay_text()
