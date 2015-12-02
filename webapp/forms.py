from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class UserForm(Form):
  username = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)]
      )
  password = StringField(
      'Password',
      validators=[DataRequired(), Length(max=225)]
      )

class CommentForm(Form):
  name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)]
      )
  text = TextAreaField(u'Comment', validators=[DataRequired()])


