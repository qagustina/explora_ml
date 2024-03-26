from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask import jsonify
from funcs import get_year
from config import SECRET_KEY

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # local 
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)
# Importar las rutas después de la creación de la app para evitar ciclos de importación circular
import routes

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    
    # Relación con el modelo Role
    role = db.relationship('Role', backref=db.backref('users'))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), unique=True, nullable=False)

class RegisterForm(FlaskForm):
    name = StringField(validators=[
                      InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "Name"})
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    email = StringField(validators=[
                        InputRequired(), Length(max=100)], render_kw={"placeholder": "Email"})
    role = StringField(validators=[
                        InputRequired(), Length(max=100)], render_kw={"placeholder": "Role"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

@ app.route('/register', methods=['GET', 'POST'])
def register():
    year = get_year()
    roles = Role.query.all()
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(
            name=form.name.data,
            username=form.username.data,
            password=hashed_password,
            email=form.email.data,
            role_id=form.role.data  # Asigna un valor al campo role_id
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form, roles=roles, current_year=year)

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

@app.route('/', methods=['GET', 'POST'])
def login():
    year = get_year()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
    return render_template('login.html', form=form, current_year=year)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
    year = get_year()
    user = current_user
    return render_template('index.html', current_user=user, current_year=year)


@app.route("/page_admin", methods=['GET', 'POST'])
@login_required
def page_admin():
    year = get_year()
    # Obtiene datos de la tabla 'usuarios'
    users = User.query.all()

    # Obtiene datos de la tabla 'role'
    roles = Role.query.all()

    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(
            name=form.name.data,
            username=form.username.data,
            password=hashed_password,
            email=form.email.data,
            role_id=form.role.data  # Asigna un valor al campo role_id
        )
        db.session.add(new_user)
        db.session.commit()

    return render_template('page_admin.html', users=users, roles=roles, form=form, current_year=year)



@app.route('/eliminar/<int:user_id>', methods=['POST'])
def eliminar_usuario(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado correctamente'})


@app.route("/get_user/<int:user_id>", methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'email': user.email,
        'role_id': user.role_id
    })

@app.route("/update_user/<int:user_id>", methods=['PUT'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.name = data.get('name', user.name)
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.role_id = data.get('role_id', user.role_id)
    db.session.commit()
    return jsonify({'message': 'Usuario actualizado correctamente'})
