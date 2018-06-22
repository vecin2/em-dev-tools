from jinja2 import Environment, FileSystemLoader, select_autoescape, meta
import os, shutil
#from jinja2 import Template

class SqlEnvironment:
    def __init__(self, templates_path):
        self.templates_path = templates_path

    def list_templates(self):
        env = Environment(
                loader = FileSystemLoader(self.templates_path),
                autoescape=select_autoescape(['html', 'xml'])
                )
        return env.list_templates('sql')


class SqlEnvFixtureBuilder:
    templates=[]
    @staticmethod
    def make():
        return SqlEnvFixtureBuilder()

    def with_path(self,templates_path):
        self.templates_path = templates_path
        return self
    
    def add_template(self, name):
        self.templates.append(name)
        return self

    def recreate(self):
        shutil.rmtree(self.templates_path)
        os.makedirs(self.templates_path)
        for template in self.templates:
            open(self.templates_path+'/'+template+'.sql','a').close()

        return SqlEnvironment(self.templates_path)

def test_list_templates_under_path():
    templates_path = os.path.dirname(os.path.realpath(__file__))+'/templates'
    sql_environment = SqlEnvFixtureBuilder.make().with_path(templates_path) \
                                                 .add_template('add-verb') \
                                                 .add_template('add-process-descriptor') \
                                                 .recreate()

    assert sql_environment.list_templates() == ['add-process-descriptor.sql','add-verb.sql']

    
