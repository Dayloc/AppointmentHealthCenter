# rutes/historial.py
from flask import Blueprint, request, jsonify
from api.models import db, HistorialMedico

historial_bp = Blueprint('historial_bp', __name__)

@historial_bp.route('/historial', methods=['GET'])
def get_all_historial():
    items = HistorialMedico.query.all()
    return jsonify([i.serialize() for i in items]), 200

@historial_bp.route('/historial/<int:id>', methods=['GET'])
def get_historial(id):
    item = HistorialMedico.query.get_or_404(id)
    return jsonify(item.serialize()), 200

@historial_bp.route('/historial', methods=['POST'])
def create_historial():
    data = request.get_json()
    item = HistorialMedico(**data)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.serialize()), 201

@historial_bp.route('/historial/<int:id>', methods=['PUT'])
def update_historial(id):
    data = request.get_json()
    item = HistorialMedico.query.get_or_404(id)
    for key, value in data.items():
        setattr(item, key, value)
    db.session.commit()
    return jsonify(item.serialize()), 200

@historial_bp.route('/historial/<int:id>', methods=['DELETE'])
def delete_historial(id):
    item = HistorialMedico.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Historial eliminado"}), 200
