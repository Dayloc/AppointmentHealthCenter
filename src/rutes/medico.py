# rutes/medico.py
from flask import Blueprint, request, jsonify
from api.models import db, Medico

medico_bp = Blueprint('medico_bp', __name__)

@medico_bp.route('/medicos', methods=['GET'])
def get_all_medicos():
    medicos = Medico.query.all()
    return jsonify([m.serialize() for m in medicos]), 200

@medico_bp.route('/medicos/<int:id>', methods=['GET'])
def get_medico(id):
    medico = Medico.query.get_or_404(id)
    return jsonify(medico.serialize()), 200

@medico_bp.route('/medicos', methods=['POST'])
def create_medico():
    data = request.get_json()
    medico = Medico(**data)
    db.session.add(medico)
    db.session.commit()
    return jsonify(medico.serialize()), 201

@medico_bp.route('/medicos/<int:id>', methods=['PUT'])
def update_medico(id):
    data = request.get_json()
    medico = Medico.query.get_or_404(id)
    for key, value in data.items():
        setattr(medico, key, value)
    db.session.commit()
    return jsonify(medico.serialize()), 200

@medico_bp.route('/medicos/<int:id>', methods=['DELETE'])
def delete_medico(id):
    medico = Medico.query.get_or_404(id)
    db.session.delete(medico)
    db.session.commit()
    return jsonify({"message": "Medico eliminado"}), 200
