import os
from collections import OrderedDict
import jinja2
from flask import Flask
from flask import render_template, request, send_from_directory, Response, Blueprint, jsonify, redirect
from jinja2 import Environment, FileSystemLoader
from flask_babel import Babel           # Flask-Babel
import lesscpy
from six import StringIO


app = Flask(__name__, static_url_path='/flask_static')
hackpad_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader('etherpad/src/themes/default/templates'),
])

app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)


def cspNonce():
    # return sha1.hex_hmac_sha1(appjet.config.requestSigningSecret, xsrfToken());
    return ''


def documentDomain():
    return '<script nonce="' + cspNonce() + '" type="text/javascript">' + \
           'try { document.domain = document.domain.split(".").slice(-2).join("."); } catch (ex) { console.log("error setting document.domain: " + ex); }</script>'


def hijackBlankClicks():
    return '\n'.join([
    '<script nonce="' + cspNonce() + '" type="text/javascript">',
    '$(document).on("click", "a[target]", function(e) {',
    '  e.preventDefault();',
    '  var newWindow = window.open("", this.target || "_blank");',
    '  if (newWindow) {',
    '    newWindow.opener = null;',
    '    newWindow.location = this.href;',
    '    newWindow.focus();',
    '  }',
    '});',
    '</script>'
  ])


def compile_less(file, minify=False, xminify=False, tabs=False, spaces=True):
    from lesscpy.lessc import parser
    from lesscpy.lessc import formatter

    class Opt(object):
        def __init__(self):
            self.minify = minify
            self.xminify = xminify
            self.tabs = tabs
            self.spaces = spaces

    p = parser.LessParser(fail_with_exc=True)
    opt = Opt()
    p.parse(file=file)
    f = formatter.Formatter(opt)
    return f.format(p)


class JinjaHelper(object):
    def __init__(self, config=dict()):
        self.js = OrderedDict()
        self.css = OrderedDict()
        self.head_meta = OrderedDict()
        self.config = config

    def includeJQuery(self):
        if 'jq' in self.js:
            return  ''

        self.js['jq'] = 'jq'
        s = '<!-- jquery -->'
        jq_ver = '1.7.2'
        scripts = [# '<script src="/static/js/less-1.4.1.min.js"></script>',
                   '<script src="/static/js/jquery-%s.js" type = "text/javascript" ></script>' % jq_ver]
        return '\n'.join(scripts)

    def includeMobileCss(self):
        s = ''      # ''<!-- mobile css -->'
        # appending css...
        if self.config.get('includeMobileCss', True):
            # FIXME: isMobileApp -> mobile-app.less
            self.includeCss('mobile-web.less')
            # request.userAgent.isIPad() -> tablet.less
            self.includeCss('phone.less')
        return s

    def includeJs(self, js_fname):
        script_link = '<script nonce="'+ cspNonce() +'" type="text/javascript" src="/static/js/%s"></script>' % js_fname
        self.js[js_fname] = script_link
        return ''

    def includeCss(self, css_fname, inplace=False):
        print 'include css', css_fname, inplace
        # <link href="/static/compressed/6b3775026387c4927ec36f91c2472744.css" rel="stylesheet" type="text/css" data-file="base.less" onError="this.loadError=true;" />
        # check css type
        _, ext = os.path.splitext(css_fname)
        if ext.lower() == '.less':
            css_link = ' <link href="/static/css/%s" rel="stylesheet/less" type="text/css" data-file="%s" onError="this.loadError=true;" />' % (css_fname, css_fname)
            # css_link = ' <link href="/static/less/%s.css" rel="stylesheet" type="text/css" data-file="%s" onError="this.loadError=true;" />' % (css_fname, css_fname)
        if ext.lower() == '.css':
            css_link = ' <link href="/static/css/%s" rel="stylesheet" type="text/css" data-file="%s" onError="this.loadError=true;" />' % (css_fname, css_fname)

        if inplace:
            # return instantly
            return css_link
        self.css[css_fname] = css_link
        return ''

    def robotsMeta(self):
        # output the robots's meta tag.
        s = '<!-- robots meta -->'
        return s

    def htmlTitle(self):
        return 'Mock Title'

    def baseHref(self):
        # return the basehref of the page
        return '/'

    def bodyId(self):
        return 'body_id'

    def bodyClasses(self):
        return ''

    def addToHead(self, head_s):
        print 'add header', head_s
        self.head_meta[head_s] = head_s
        return ''

    def headExtra(self):
        print self.head_meta.keys(), '-----------------'
        s = '\n'.join(self.head_meta.keys())
        return s

    def documentDomain(self):
        return documentDomain()

    def addClientVars(self, options):
        return ''

    def xsrfToken(self):
        return ''

    def xsrfTokenElement(self):
        return ''

    def cssIncludes(self):
        # dump all the css include tag.
        s = '\n'.join(self.css.values())
        return s

    def jsIncludes(self):
        if 'jq' in self.js:
            del self.js['jq']
        return '\n'.join(self.js.values())

    @property
    def scripts(self):
        return self.js

    def cdn(self):
        return '/cdn'

    def clientVarsScript(self):
        x = '''{"experiment":"homepage-v3","xsrf":"e5298ce5519fdaef","isDogfood":true,"cdn":""}'''
        return '\n'.join([
            '<script type="text/javascript" nonce="' + cspNonce() + '">',
            '  // <![CDATA[',
            'var clientVars = ' + x + ';',
            '  // ]]>',
            '</script>'
        ])

    def track(self):
        output = env.get_template('track.j2.html').render(helpers=JinjaHelper(), request=request)
        #return utils.renderTemplateAsString("track.ejs");
        print (output)
        return output

    def tailExtra(self):
        return ''

    def profileTicks(self):
        return ''

    def hijackBlankClicks(self):
        return hijackBlankClicks()

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

    """
        Flask's Helper, for some logic hard to express in Template Jinja2
    """
    def getMenu(self):
        """
        :return: a menu hash used in macro button
        """


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

env = Environment(extensions=['jinja2.ext.i18n', 'jinja2.ext.do'], loader=hackpad_loader)
env.filters['clear'] = clear_output
env.filters['encodeURIComponent'] = encode_uri_component

# i18n
# translations = get_gettext_translations()
env.install_null_translations()

# env.install_gettext_translations(gettext.translations('hackpad'))

"""
    deal with css
"""


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/static/<path:filename>')
def static_proxy(filename):
    # send_static_file will guess the correct MIME type
    # FIXME: read the SLEIPNIR_ROOT from settings.
    # view-source:http://localhost:8080/uml/static/examples/grapheditor/www/index.html
    static_path = os.path.abspath(os.path.join('etherpad', 'src', 'static'))
    # print "---------------------", static_path
    return send_from_directory(static_path, filename)

@app.route('/cdn/static/<path:filename>')
def static_cdn(filename):
    # default static file which can use cdn
    static_path = os.path.abspath(os.path.join('etherpad', 'src', 'static'))
    # print "---------------------", static_path
    return send_from_directory(static_path, filename)


@app.route('/static/less/<path:filename>.css')
def static_less(filename):
    """
        1. FIXME: add cdn support in less, back
                home_ejs.less:  background: url(<%=helpers.cdn()%>/static/img/main.jpg);
    """
    import lesscpy
    from six import StringIO
    # FIXME: try support less in node.js side.(pre-compiled)
    # default static file which can use cdn
    static_path = os.path.abspath(os.path.join('etherpad', 'src', 'static',  'css'))
    # print "---------------------", static_path
    fname = os.path.join(static_path, filename)
    with open(fname, 'rb') as fh:
        s = compile_less(fh, minify=False)
    return Response(s, mimetype='text/css')
    #return send_from_directory(static_path, filename)


@app.route('/static/css/<path:filename>')
def static_css(filename):
    # default static file which can use cdn
    static_path = os.path.abspath(os.path.join('etherpad', 'src', 'static', 'css'))
    # print "---------------------", static_path
    return send_from_directory(static_path, filename)


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
    output = env.get_template('main/home.j2.html').render(helpers=JinjaHelper(), request=request)
    return output


@app.route('/pad/<name>')
def pad_editor(name=None):
    """
    By default three type of editor.

        - pad/editor_desktop.ejs
        - pad/editor_ios.ejs
        - pad/editor_full.ejs

    """
    bodyHtml = env.get_template('pad/editor_full.j2.html').render(
        helpers=JinjaHelper(), request=request
    )
    output = env.get_template('html.j2.html').render(
        bodyHtml = bodyHtml, helpers=JinjaHelper(), request=request
    )
    return output

"""
    EtherPad(Java), which Hackpad forked from.
    The URL of
"""
ep = Blueprint(
    "etherpad", __name__, url_prefix='/ep',
    template_folder='templates', # registers airflow/plugins/templates as a Jinja template folder
    static_folder='static',
    static_url_path='/static/test_plugin')


@ep.route('/account/login-or-signup', methods=['POST'])
def login_or_signup():
    # read from a html FORM post.
    # email=admin%40local.com&xsrf=e5298ce5519fdaef
    # {"signup":false} if .....
    res_data = {
        "signup": False
    }
    # ep/account/login-or-signup
    return jsonify(res_data)

@ep.route('/account/signin', methods=['POST'])
def account_signin():
    # xsrf=adbb82dd8935498b&email=admin%40local.com&password=123456&rememberMe=1&cont=http%3A%2F%2Flocalhost%3A9000%2F&name=
    # login ok
    res_data = {
        "success": True,
        "cont": '/'
    }
    # ep/account/login-or-signup
    return jsonify(res_data)

# register blueprint
app.register_blueprint(ep)


if __name__ == '__main__':
    app.run(debug=True, )
