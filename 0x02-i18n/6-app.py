#!/usr/bin/env python3

from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user(user_id):
    user = users.get(user_id)
    if user:
        return user
    return None

def get_locale():
    # Check if locale is in URL parameters
    loc = request.args.get('locale')
    if loc and loc in app.config['LANGUAGES']:
        return loc

    # Check if user is logged in and has a preferred locale
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    # Check for locale in the request header
    header_locale = request.headers.get('Accept-Language')
    if header_locale:
        supported_locales = app.config['LANGUAGES']
        # Split the Accept-Language header by commas and find the first matching locale
        for lang in header_locale.split(','):
            lang = lang.split(';')[0].strip()
            if lang in supported_locales:
                return lang

    # Default locale
    return app.config['BABEL_DEFAULT_LOCALE']

@app.before_request
def before_request():
    user_id = request.args.get("login_as")
    g.user = get_user(int(user_id)) if user_id else None

@app.route('/')
def index():
    return render_template('6-index.html')

if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
