from flask import Blueprint, jsonify, current_app, request, abort
from models import Pet
import jwt
from datetime import datetime, timedelta, timezone
from decorator import token_required

api_bp = Blueprint("api", __name__, template_folder="templates", static_folder="static")  # создаем объект Blueprint


@api_bp.route('/')
def api_index():
    return jsonify({"status": 200})


@api_bp.route('/get_pets')
@token_required
def get_pets():
    pets = Pet.query.all()
    result = {}
    for pet in pets:
        result[pet.id] = {"name": pet.name,
                          "age": pet.age,
                          "description": pet.description,
                          "pet_type": pet.pet_type}
    return jsonify({"pets": result})


@api_bp.route('/auth', methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        email = request.json.get("email")
        password = request.json.get("password")
        exp = datetime.now(tz=timezone.utc) + timedelta(hours=1)
        token = jwt.encode(dict(email=email, password=password, exp=exp), current_app.secret_key,
                           algorithm="HS256")
        return {"status": "token generated successfully", "token": token}
    return abort(405)
