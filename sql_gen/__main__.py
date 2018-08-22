from jinja2 import Environment, FileSystemLoader, select_autoescape, meta, Template
from sql_gen.template_source import TemplateSource
from sql_gen.prompter import Prompter
from sql_gen.filter_loader import load_filters
from sql_gen_app import run_app
 
##main
def main():
    run_app()

if __name__ == '__main__':
    main()
