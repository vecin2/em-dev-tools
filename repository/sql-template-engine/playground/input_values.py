from jinja2 import Environment, FileSystemLoader, select_autoescape, meta, Template
from template_source import TemplateSource

env = Environment(
            loader=FileSystemLoader('/home/dgarcia/dev/python/em_dev_tools/repository/sql-template-engine/playground/templates/'),
            autoescape=select_autoescape(['html', 'xml'])
                )
template = env.get_template('add_process_descriptor.html')
template_source = env.loader.get_source(env, 'add_process_descriptor.html')[0]
parsed_content= env.parse(template_source)

template_source=TemplateSource(parsed_content)
default=template_source.get_default_value('config_id')
print('type', type(default))
print('default value is: '+ default.encode('ascii','ignore'))
print('********',parsed_content.body[0])
print('*****',parsed_content.body[0].nodes[7])

template_vars =meta.find_undeclared_variables(parsed_content)
context ={}
for current in template_vars:
    default_unicode= template_source.get_default_value(current)

    prompt_text=current 
    if default_unicode:
        default_value= default_unicode.encode('ascii','ignore')
        prompt_text = prompt_text + " (default is "+default_value+")"
    var =raw_input(prompt_text+":")
    print("you entered ", var)
    if var:
        context[current] = var

print(template.render(context))

