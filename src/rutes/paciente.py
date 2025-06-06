# rutes/paciente.py
from flask import Blueprint, request, jsonify
from api.models import db, Paciente

paciente_bp = Blueprint('paciente_bp', __name__)

@paciente_bp.route('/pacientes', methods=['GET'])
def get_all_pacientes():
    pacientes = Paciente.query.all()
    return jsonify([p.serialize() for p in pacientes]), 200

@paciente_bp.route('/pacientes/<int:id>', methods=['GET'])
def get_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    return jsonify(paciente.serialize()), 200

@paciente_bp.route('/pacientes', methods=['POST'])
def create_paciente():
    data = request.get_json()
    paciente = Paciente(**data)
    db.session.add(paciente)
    db.session.commit()
    return jsonify(paciente.serialize()), 201

@paciente_bp.route('/pacientes/<int:id>', methods=['PUT'])
def update_paciente(id):
    data = request.get_json()
    paciente = Paciente.query.get_or_404(id)
    for key, value in data.items():
        setattr(paciente, key, value)
    db.session.commit()
    return jsonify(paciente.serialize()), 200

@paciente_bp.route('/pacientes/<int:id>', methods=['DELETE'])
def delete_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    return jsonify({"message": "Paciente eliminado"}), 200