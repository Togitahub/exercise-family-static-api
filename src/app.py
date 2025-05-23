"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

@app.route('/members/<int:id>', methods=['GET'])
def handle_member(id):
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify({"msg": "Miembro no encontrado"}), 404
    
    return jsonify(member), 200

@app.route('/members', methods=['POST'])
def handle_add_member():
    request_body = request.json
    if request_body and "first_name" in request_body and "age" in request_body and "lucky_numbers" in request_body:
        if isinstance(request_body["lucky_numbers"], list):
            member = jackson_family.add_member(request_body)
            return jsonify(member), 200
        else:
            return jsonify({"msg": "lucky_numbers debe ser una lista"}), 400
    else:
        return jsonify({"msg": "El cuerpo de la solicitud debe contener first_name, age y lucky_numbers"}), 400


@app.route('/members/<int:id>', methods=['DELETE'])
def handle_delete_member(id):
    if jackson_family.get_member(id) is None:
        return jsonify({"msg": "Miembro no encontrado"}), 404
    else:
        jackson_family.delete_member(id)
        return jsonify({"done": True}), 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
