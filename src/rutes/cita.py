from flask import Blueprint, request, jsonify
from api.models import db, Cita

cita_bp = Blueprint('cita_bp', __name__)

# Obtener todas las citas
@cita_bp.route('/citas', methods=['GET'])
def get_all_citas():
    citas = Cita.query.all()
    return jsonify([c.serialize() for c in citas]), 200

# Obtener una cita por ID
@cita_bp.route('/citas/<int:id>', methods=['GET'])
def get_cita(id):
    cita = Cita.query.get_or_404(id)
    return jsonify(cita.serialize()), 200

# Crear una nueva cita
@cita_bp.route('/citas', methods=['POST'])
def create_cita():
    data = request.get_json()
    nueva_cita = Cita(
        fecha_hora=data.get('fecha_hora'),
        estado=data.get('estado'),
        tipo=data.get('tipo'),
        paciente_id=data.get('paciente_id'),
        medico_id=data.get('medico_id')
    )
    db.session.add(nueva_cita)
    db.session.commit()
    return jsonify(nueva_cita.serialize()), 201

# Actualizar una cita existente
@cita_bp.route('/citas/<int:id>', methods=['PUT'])
def update_cita(id):
    data = request.get_json()
    cita = Cita.query.get_or_404(id)

    cita.fecha_hora = data.get('fecha_hora', cita.fecha_hora)
    cita.estado = data.get('estado', cita.estado)
    cita.tipo = data.get('tipo', cita.tipo)
    cita.paciente_id = data.get('paciente_id', cita.paciente_id)
    cita.medico_id = data.get('medico_id', cita.medico_id)

    db.session.commit()
    return jsonify(cita.serialize()), 200

# Eliminar una cita
@cita_bp.route('/citas/<int:id>', methods=['DELETE'])
def delete_cita(id):
    cita = Cita.query.get_or_404(id)
    db.session.delete(cita)
    db.session.commit()
    return jsonify({"message": "Cita eliminada"}), 200
