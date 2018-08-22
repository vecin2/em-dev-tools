from jinja2 import Environment, FileSystemLoader, select_autoescape, meta, Template
from sql_gen.template_source import TemplateSource
from sql_gen.prompter import Prompter
from sql_gen.environment_selection import TemplateSelector, EMTemplatesEnv
import argparse
from sql_module.em_project import SQLTask


##main
def run_app():
 # construct the argument parse and parse the arguments
    args = parse_args();
    sql_task_path = args["path"]
    env = EMTemplatesEnv().get_env()
    template_selector = TemplateSelector()
    template_source= template_selector.select_template(env)
    prompter = Prompter(template_source)
    context = prompter.build_context()
    template = env.get_template(template_source.template_name)

    template_parsed =template.render(context)
    print(template_parsed)
    sql_task = SQLTask.make().path(sql_task_path).with_table_data(template_parsed);
    sql_task.write()
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

