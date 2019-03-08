from app import app
from .inter import inter
from .admin import admin
from .wxweb import wxweb

app.register_blueprint(inter, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(wxweb, url_prefix='/wxweb')


