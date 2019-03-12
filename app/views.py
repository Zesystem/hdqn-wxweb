from app import app
from .inter import inter
from .admin import admin
from .wxweb import wxweb
from .public import public
from flask import render_template

app.register_blueprint(inter, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(wxweb, url_prefix='/wxweb')
app.register_blueprint(public, url_prefix='/public')


@app.errorhandler(401)
def unauthorized_access(error):
    return render_template('public/401.html'), 401

@app.errorhandler(404)
def page_not_found(error):
    return render_template('public/404.html'), 404