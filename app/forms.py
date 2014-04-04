from flask.ext.wtf import Form
from wtforms import TextAreaField, SelectField, TextField, FileField, BooleanField
from wtforms.validators import Optional, Required, regexp



class loginForm(Form):
    username = TextField(u'')


    
    


