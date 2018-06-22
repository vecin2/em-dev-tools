from jinja2 import Environment, FileSystemLoader, select_autoescape, meta, Template

env = Environment(
            loader=FileSystemLoader('/home/dgarcia/dev/python/em_dev_tools/repository/sql-template-engine/templates_old'),
            autoescape=select_autoescape(['html', 'xml'])
                )
template = env.get_template('add-verb.html')
print (template.render(verb_id='inlineView'))
template_source = env.loader.get_source(env, 'add-verb.html')[0]
print("this is template source", template_source)
parsed_content = env.parse(template_source)
print("the is the parsed content",parsed_content)
template_vars = meta.find_undeclared_variables(parsed_content)
print(list(template_vars)[0])
print(template_vars)
#template = Template('Hello {{ name }}!')
#print(template.render(name='John Doe'))
#ast=template.render(verb_id='inlineView')
#print(template.globals['namespace'].size)
#print(ast);
#print (template.globals)
#print (template.context)

