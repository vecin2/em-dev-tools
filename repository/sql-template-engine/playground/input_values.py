from jinja2 import Environment, FileSystemLoader, select_autoescape, meta, Template

env = Environment(
            loader=FileSystemLoader('/home/dgarcia/dev/python/em_dev_tools/repository/sql-template-engine/playground/templates/'),
            autoescape=select_autoescape(['html', 'xml'])
                )
template = env.get_template('add_process_descriptor.html')
template_source = env.loader.get_source(env, 'add_process_descriptor.html')[0]
parsed_content= env.parse(template_source)
template_vars =meta.find_undeclared_variables(parsed_content)
context ={}
for current in template_vars:
    var =raw_input(current+":")
    print("you entered ", var)
    context[current] = var

print(template.render(context))

