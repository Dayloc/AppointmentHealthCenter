from flask import Blueprint, request, jsonify
from api.models import db, User,Paciente
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

user_bp = Blueprint('user_bp', __name__)

# Obtener todos los usuarios
bcrypt = Bcrypt()


@user_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200

# Obtener un usuario por ID


@user_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.serialize()), 200

# Crear un nuevo usuario


@user_bp.route('/users/register', methods=['POST'])
def create_user():
    data = request.get_json()

    try:
        nombre = data.get("nombre")
        email = data.get("email")
        password = data.get("password")
        tipo_usuario = data.get("tipo_usuario")

        if not all([nombre, email, password, tipo_usuario]):
            return jsonify({"msg": "Faltan datos obligatorios"}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Crear usuario
        new_user = User(
            nombre=nombre,
            email=email,
            password=hashed_password,
            tipo_usuario=tipo_usuario
        )
        db.session.add(new_user)
        db.session.flush()  # Para obtener el ID antes de hacer commit

        # Si es paciente, registrar también en la tabla pacientes
        if tipo_usuario == "paciente":
            direccion = data.get("direccion")
            telefono = data.get("telefono")
            fecha_nacimiento = data.get("fecha_nacimiento")
            genero = data.get("genero")
            tipo_sangre = data.get("tipo_sangre")

            nuevo_paciente = Paciente(
                direccion=direccion,
                telefono=telefono,
                fecha_nacimiento=fecha_nacimiento,
                genero=genero,
                tipo_sangre=tipo_sangre,
                user_id=new_user.id
            )
            db.session.add(nuevo_paciente)

        db.session.commit()

        access_token = create_access_token(identity=new_user.id)

        return jsonify({
            "msg": "Usuario creado exitosamente",
            "access_token": access_token,
            "user": new_user.serialize()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# login de usuario


@user_bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    print("Datos recibidos:", data)

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    print("Usuario encontrado:", user)

    if user and bcrypt.check_password_hash(user.password, password):
        print("Password verificado correctamente")
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "access_token": access_token,
            "user": user.serialize()
        }), 200
    else:
        print("Credenciales inválidas")
        return jsonify({"msg": "Credenciales inválidas"}), 401


# Actualizar un usuario existente


@user_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)

    user.nombre = data.get('nombre', user.nombre)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    user.tipo_usuario = data.get('tipo_usuario', user.tipo_usuario)

    db.session.commit()
    return jsonify(user.serialize()), 200

# Eliminar un usuario


@user_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200
