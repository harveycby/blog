from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
from blog.models import User


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    submit = SubmitField('登录') 

    def validate_username(self, field):
        if field.data and not User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名未注册')

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')