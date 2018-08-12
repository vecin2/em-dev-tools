from jinja2 import Environment, FileSystemLoader, select_autoescape, meta, Template
from sql_gen.template_source import TemplateSource
from sql_gen.prompter import Prompter
import os,sys



class TemplateOption():
    def __init__(self,id, name):
        self.id =id
        self.name =name

class TemplateSelector():
    def select_template(self, env):
        template_list = env.list_templates(".sql")
        template_option_list=[]
        for counter, template in enumerate(template_list):
            template_option =TemplateOption(counter, template)
            template_option_list.append(template_option)
            
        for template_option in template_option_list:
            print(str(template_option.id) + ". " +template_option.name)

        template_number = raw_input("Please select template to parse: ")

        template_name = self.get_template_by_id(template_option_list, template_number).name
        return TemplateSource(template_name,env)
    

    def get_template_by_id(self, template_option_list, template_number):
        for template_option in template_option_list:
            if template_number == str(template_option.id):
                return template_option
        return None

def description(value, description):
    return value


env = Environment(
                loader=FileSystemLoader('/home/dgarcia/dev/python/em_dev_tools/sql_gen/templates'),
                autoescape=select_autoescape(['html', 'xml']))
env.filters['description']=description

template_selector = TemplateSelector()
template_source= template_selector.select_template(env)

prompter = Prompter(template_source)
context = prompter.build_context()
template = template_source.get_template()
print(template.render(context))

