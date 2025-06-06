import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import (
    db,
    User,
    Paciente,
    Medico,
    Cita,
    Analisis,
    HistorialMedico,
    FarmacoAlergeno
)

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    admin = Admin(app, name='VidaPlena Admin', template_mode='bootstrap3')

    # Agregar modelos al panel de administración
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Paciente, db.session))
    admin.add_view(ModelView(Medico, db.session))
    admin.add_view(ModelView(Cita, db.session))
    admin.add_view(ModelView(Analisis, db.session))
    admin.add_view(ModelView(HistorialMedico, db.session))
    admin.add_view(ModelView(FarmacoAlergeno, db.session))
