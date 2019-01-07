from flask_wtf import  FlaskForm
from wtforms.validators import Required
from wtforms import StringField,SubmitField

class NameForm(FlaskForm):
    name = StringField('What is you name?',validators=[Required()])
    submit = SubmitField('Submit')

