import uuid 
import json
import os

from flask import g, request, jsonify, send_file, abort, url_for
from flask_expects_json import expects_json
import jsonschema

from app import app
from app import db
from app import schemas
from app.models import User, File
from app.logic import convert_and_save, get_path

@app.route("/create_user", methods=["post"])
@expects_json(schemas.create_user_request)
def create_user():
    username = g.data.get("username")
    user = User(username)
    db.session.add(user)
    db.session.flush()
    db.session.refresh(user)
    db.session.commit()
    return {"user_id":user.id, "token": str(uuid.UUID(bytes=user.token))}

@app.route("/create_audio", methods=["post"])
def create_audio():
    response = None
    try:
        user_data = json.loads(request.form.get('user_data'))
        jsonschema.validate(user_data, schemas.create_audio_request)
    except json.decoder.JSONDecodeError as err:
        response = jsonify({'message': err.message}) 
        response.status_code = 400
    except jsonschema.ValidationError as err:
        response = jsonify({'message': err.message}) 
        response.status_code = 400
    if response:
        return response
    
    if not db.session.query(User).filter(
        User.id == user_data["user_id"]).filter(
            User.token == uuid.UUID(user_data["token"]).bytes).first():
            abort(403)
    
    file = request.files['file']
    
    file_uuid = convert_and_save(file)
    file = File(user_data["user_id"], file_uuid)
    db.session.add(file)
    db.session.commit()
    return url_for("get_record", _external=True) + f"?id={str(file_uuid)}&user={user_data['user_id']}"


@app.route("/record", methods=["get"])
def get_record():
    file_uuid = request.args.get("id")
    user_id = request.args.get("user")
    try:
        jsonschema.validate(file_uuid, {"type":"string", "format":"uuid"})
        user_id = int(user_id)
    except (jsonschema.ValidationError, ValueError, TypeError) as err:
        responce = jsonify({"message":err.message})
        responce.status_code = 400
        return responce
    
    file_uuid = uuid.UUID(file_uuid)
    
    file_obj = db.session.query(File).filter(File.id == file_uuid.bytes).filter(File.created_by_id == user_id).first()
    if not file_obj:
        abort(404)
    
    return send_file(os.path.abspath(get_path(file_uuid)), as_attachment=True)
        
    
    
