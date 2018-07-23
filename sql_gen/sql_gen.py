from jinja2 import Environment, FileSystemLoader, select_autoescape, meta, Template
from sql_gen.template_source import TemplateSource

def description(value, description):
    return value

env = Environment(
            loader=FileSystemLoader('/home/dgarcia/dev/python/em_dev_tools/repository/sql-template-engine/playground/templates/'),
            autoescape=select_autoescape(['html', 'xml'])
                )
env.filters['description']=description
template = env.get_template('add_process_descriptor.sql')
template_source = env.loader.get_source(env, 'add_process_descriptor.sql')[0]
parsed_content= env.parse(template_source)

template_source=TemplateSource(parsed_content)
print('*****',parsed_content.body[0].nodes[9])

template_vars =meta.find_undeclared_variables(parsed_content)
context ={}
for current in template_vars:
    desc_unicode = template_source.get_description(current)
    default_unicode= template_source.get_default_value(current)

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

