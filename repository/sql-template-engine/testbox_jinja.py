from jinja2 import Environment, FileSystemLoader, select_autoescape, meta

#from jinja2 import Template

env = Environment(
            #loader=PackageLoader('', 'templates'),
            loader = FileSystemLoader('/home/dgarcia/dev/python/em_dev_tools/my_project/repository/sql-template-engine/templates'),
                autoescape=select_autoescape(['html', 'xml'])
                )
template = env.get_template('add-verb.html')
print template.render(verb_id='inlineView')
template_source = env.loader.get_source(env, 'add-verb.html')[0]
parsed_content = env.parse(template_source)
print(parsed_content)
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

