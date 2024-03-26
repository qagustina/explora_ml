#from application.__init__ import app, db 
from app import app, db
#from application import User, Role  # Importa tus modelos aquí

# Esto crea las tablas según los modelos definidos
with app.app_context():
    db.create_all()

print("Base de datos inicializada.")
