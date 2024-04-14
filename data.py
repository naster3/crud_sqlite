from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    content = StringField('Content', validators=[DataRequired()])
    done = BooleanField('Done')
    fecha_creacion = DateField('Fecha de Creación', format='%Y-%m-%d', validators=[DataRequired()])
