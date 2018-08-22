from jinja2 import Environment, FileSystemLoader, select_autoescape, meta, Template
from sql_gen.template_source import TemplateSource
from sql_gen.prompter import Prompter
from sql_gen.filter_loader import load_filters
import filters.description
from filters.description import DescriptionFilter
import os,sys
import argparse

#sys.path.append("/home/dgarcia/dev/python/em_dev_tools/sql_gen")
class TemplateOption(object):
    def __init__(self,id, name):
        self.id =id
        self.name =name

class TemplateSelector():
    def select_template(self, env):
        template_list = env.list_templates(".sql")
        self.create_options(template_list)
        self.show_options()

        template_number = self.prompt_to_select_template()    
        template_name = self.get_option_by_id(template_number).name
        return self.build_template_source(template_name,env)
    
    def create_options(self, template_list):
        self.template_option_list=[]
        for counter, template in enumerate(template_list):
            template_option =TemplateOption(counter, template)
            self.template_option_list.append(template_option)
        return self.template_option_list

    def show_options(self):
        for template_option in self.template_option_list:
            print(str(template_option.id) + ". " +template_option.name)
    def prompt_to_select_template(self):
        template_number = raw_input("Please select template to parse: ")
        while self.get_option_by_id(template_number) is None:
            template_number = raw_input("Please select template to parse: ")
            self.show_options()
        return template_number

    def get_option_by_id(self, template_number):
        for template_option in self.template_option_list:
            if template_number == str(template_option.id):
                return template_option
        return None

    def build_template_source(self, template_name, env):
        source = env.loader.get_source(env,template_name)[0]
        template_source = TemplateSource(env.parse(source))
        template_source.template_name = template_name
        return template_source


##main
def run_app():
 # construct the argument parse and parse the arguments
    args = parse_args();
    env = Environment(
                    loader=FileSystemLoader('/home/dgarcia/dev/python/em_dev_tools/sql_gen/templates'),
                    autoescape=select_autoescape(['html', 'xml']))

    load_filters(env)
    template_selector = TemplateSelector()
    template_source= template_selector.select_template(env)
    prompter = Prompter(template_source)
    context = prompter.build_context()
    template = env.get_template(template_source.template_name)

    print(template.render(context))
#    EMProject.add_sql_task(TableDataTask.path(sql_task_path)
#                                  .with_table_data(parsed_template))
#                                  
#
def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True, help="Its the relative path from  $CORE_HOME where the sql ask will be written to, e.g. modules/GSCCoreEntites...")
    return vars(ap.parse_args())
    

if __name__ == '__main__':
    main()

