
class DescriptionFilter(object):
    def __init__(self, jinja_filter):
        self.filter = jinja_filter;

    def apply(self, display_text):
        return self.filter.args[0].value
