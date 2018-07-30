from jinja2 import Environment, FileSystemLoader, select_autoescape, meta, Template
from sql_gen.template_source import TemplateSource
import os,sys

class TemplateOption():
    def __init__(self,id, name):
        self.id =id
        self.name =name


class TemplateSelector():
    def init(self):
        env = Environment(
                loader=FileSystemLoader('/home/dgarcia/dev/python/em_dev_tools/repository/sql-template-engine/playground/templates/'),
                autoescape=select_autoescape(['html', 'xml'])
                )

        env.filters['description']=description
        return env

def select_template(env):
    template_list = env.list_templates()
    template_option_list=[]
    for counter, template in enumerate(template_list):
        template_option =TemplateOption(counter, template)
        template_option_list.append(template_option)
        
    for template_option in template_option_list:
        print(str(template_option.id) + ". " +template_option.name)

    template_number = raw_input("Please select template to parse: ")

    return get_template_by_id(template_option_list, template_number).name

def get_template_by_id(template_option_list, template_number):
    for template_option in template_option_list:
        if template_number == str(template_option.id):
            return template_option
    return None

def description(value, description):
    return value

template_selector = TemplateSelector()

env =template_selector.init()
template_name= select_template(env);
template = env.get_template(template_name)
template_source = env.loader.get_source(env,template_name)[0]
parsed_content= env.parse(template_source)

template_source=TemplateSource(parsed_content)

template_vars =meta.find_undeclared_variables(parsed_content)
context ={}
for current in template_vars:
    desc_unicode = template_source.get_description(current)
    default_unicode= template_source.get_default_value(current)
    print("description is "+ desc_unicode)
    print("default is "+ default_unicode)

    prompt_text=current 
    if desc_unicode:
        prompt_text = desc_unicode.encode('ascii','ignore')
    if default_unicode:
        default_value= default_unicode.encode('ascii','ignore')
        prompt_text = prompt_text + " (default is "+default_value+")"
    var =raw_input(prompt_text+":")
    print("you entered ", var)
    if var:
        context[current] = var

print(template.render(context))

