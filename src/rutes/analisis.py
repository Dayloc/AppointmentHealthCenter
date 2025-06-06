# rutes/analisis.py
from flask import Blueprint, request, jsonify
from api.models import db, Analisis

analisis_bp = Blueprint('analisis_bp', __name__)

@analisis_bp.route('/analisis', methods=['GET'])
def get_all_analisis():
    items = Analisis.query.all()
    return jsonify([i.serialize() for i in items]), 200

@analisis_bp.route('/analisis/<int:id>', methods=['GET'])
def get_analisis(id):
    item = Analisis.query.get_or_404(id)
    return jsonify(item.serialize()), 200

@analisis_bp.route('/analisis', methods=['POST'])
def create_analisis():
    data = request.get_json()
    item = Analisis(**data)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.serialize()), 201

@analisis_bp.route('/analisis/<int:id>', methods=['PUT'])
def update_analisis(id):
    data = request.get_json()
    item = Analisis.query.get_or_404(id)
    for key, value in data.items():
        setattr(item, key, value)
    db.session.commit()
    return jsonify(item.serialize()), 200

@analisis_bp.route('/analisis/<int:id>', methods=['DELETE'])
def delete_analisis(id):
    item = Analisis.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Análisis eliminado"}), 200
