from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin

class LoginForm(FlaskForm):
    """管理员登陆表单"""
    account = StringField(
        label='Account',
        validators=[
            DataRequired('Please input your account!')
        ],
        description='Account',
        render_kw={
            'class' : 'input_self',
            'id' : 'account',
            'placeholder' : 'Please input your account!',
            #'required' : 'required'
        }
    )

    password = PasswordField(
        label='Password',
        validators=[
            DataRequired('Please input your password!')
        ],
        description='Password',
        render_kw={
            'class' : 'input_self',
            'id' : 'password',
            'placeholder' : 'Please input your password!',
            #'required' : "required"
        }
    )

    submit = SubmitField(
        label='Login',
        render_kw={
            'class' : "finish_btn",
            'id' : 'finish',
            'value' : 'Login'
        }
    )

    def validate_account(self, field):
        this_account = field.data
        admin = Admin.query.filter(Admin.account == this_account).first()
        if admin is None:
            raise ValidationError('Account does not exist!')
    
    def validate_password(self, field):
        pwd_len = len(field.data)
        if pwd_len < 6 or pwd_len > 16:
            raise ValidationError('Length of password must be in 6 ~ 10 bits')