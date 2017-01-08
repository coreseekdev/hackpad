from collections import OrderedDict
import jinja2
from flask import Flask
from flask import render_template
from jinja2 import Environment, FileSystemLoader
from flask_babel import Babel           # Flask-Babel


app = Flask(__name__)
hackpad_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader('etherpad/src/themes/default/templates'),
])

app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)


class JinjaHelper(object):
    def __init__(self):
        self.js = OrderedDict()
        self.css = OrderedDict()

    def includeJQuery(self):
        return ''

    def includeMobileCss(self):
        return ''

    def includeJs(self, js_fname):
        self.js[js_fname] = js_fname

    def includeCss(self, css_fname):
        self.css[css_fname] = css_fname

    def robotsMeta(self):
        # output the robots's meta tag.
        return ''

    def htmlTitle(self):
        return 'Mock Title'

    def baseHref(self):
        # return the basehref of the page
        return '/'

    def bodyId(self):
        return 'body_id'

    def bodyClasses(self):
        return ''

    def includeJQuery(self):
        # the jQuery's script
        return ''

    def headExtra(self):
        return ''

    def documentDomain(self):
        return ''

    def addClientVars(self, options):
        return ''

    def xsrfToken(self):
        return ''

    def xsrfTokenElement(self):
        return ''

    def cssIncludes(self):
        # dump all the css include tag.
        return ''

    def jsIncludes(self):
        return ''

    @property
    def scripts(self):
        return self.js

    def cdn(self):
        return 'http://cdn.baidu.com'

    def clientVarsScript(self):
        return ''

    def track(self):
        return ''

    def tailExtra(self):
        return ''

    def profileTicks(self):
        return ''

    def hijackBlankClicks(self):
        return ''

    def disableOffline(self):
        return ''

    def addSmartAppBanner(self):
        return ''

    def setRobotsPolicy(self, option):
        return ''

    def cspNonce(self):
        return ''

    def suppressGA(self):
        return ''

    def setHtmlTitle(self):
        return ''

    def addBodyClass(self):
        return ''

def clear_output(s):
    if s is None:
        return ''
    return s


def encode_uri_component(s):
    import urllib
    if type(s) == unicode:
        return urllib.quote(s.encode("utf-8"))
    else:
        return urllib.quote(s)

env = Environment(extensions=['jinja2.ext.i18n'], loader=hackpad_loader)
env.globals['helpers'] = JinjaHelper()
env.filters['clear'] = clear_output
env.filters['encodeURIComponent'] = encode_uri_component

# i18n
# translations = get_gettext_translations()
env.install_null_translations()

# env.install_gettext_translations(gettext.translations('hackpad'))

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/html/bare')
def bare_html():
    """18n1
    try convert page.ejs to Jinja2's template
    """
    output = env.get_template('html.j2.html').render()
    return output

@app.route('/html/home')
def home_html():
    """18n1
    try convert page.ejs to Jinja2's template
    """
    output = env.get_template('main/home.j2.html').render()
    return output

@app.route('/page/')
@app.route('/hello/<name>')
def page(name=None):
    """18n1
    try convert page.ejs to Jinja2's template
    """
    output = env.get_template('page.j2.html').render(
        name=name
    )
    return output


if __name__ == '__main__':
    app.run(debug=True, )
