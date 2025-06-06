# rutes/farmaco.py
from flask import Blueprint, request, jsonify
from api.models import db, FarmacoAlergeno

farmaco_bp = Blueprint('farmaco_bp', __name__)

@farmaco_bp.route('/farmacos', methods=['GET'])
def get_all_farmacos():
    items = FarmacoAlergeno.query.all()
    return jsonify([i.serialize() for i in items]), 200

@farmaco_bp.route('/farmacos/<int:id>', methods=['GET'])
def get_farmaco(id):
    item = FarmacoAlergeno.query.get_or_404(id)
    return jsonify(item.serialize()), 200

@farmaco_bp.route('/farmacos', methods=['POST'])
def create_farmaco():
    data = request.get_json()
    item = FarmacoAlergeno(**data)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.serialize()), 201

@farmaco_bp.route('/farmacos/<int:id>', methods=['PUT'])
def update_farmaco(id):
    data = request.get_json()
    item = FarmacoAlergeno.query.get_or_404(id)
    for key, value in data.items():
        setattr(item, key, value)
    db.session.commit()
    return jsonify(item.serialize()), 200

@farmaco_bp.route('/farmacos/<int:id>', methods=['DELETE'])
def delete_farmaco(id):
    item = FarmacoAlergeno.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Fármaco eliminado"}), 200
