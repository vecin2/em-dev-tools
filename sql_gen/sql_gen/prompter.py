class Prompter(object):
    def __init__(self, template_source):
        self.template_source = template_source

    def build_context(self):
        template_vars = self.template_source.find_undeclared_variables()

        context ={}
        for current in template_vars:
            desc_unicode = self.template_source.get_description(current)
            default_unicode= self.template_source.get_default_value(current)

            prompt_text=current 
            if desc_unicode:
                prompt_text = desc_unicode.encode('ascii','ignore')
            if default_unicode:
                default_value= default_unicode.encode('ascii','ignore')
                prompt_text = prompt_text + " (default is "+default_value+")"
            var =raw_input(prompt_text+":")
            if var:
                context[current] = var
        return context

