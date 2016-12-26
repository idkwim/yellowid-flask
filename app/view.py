from app import app
from flask import request, jsonify
from .manager import APIAdmin


def process_fail():
    message = APIAdmin.process("fail")
    return jsonify(message)


@app.route("/api/keyboard", methods=["GET"])
def yellow_keyboard():
    message = APIAdmin.process("home")
    return jsonify(message), 200


@app.route("/api/message", methods=["POST"])
def yellow_message():
    try:
        message = APIAdmin.process("message", request.json)
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/friend", methods=["POST"])
def yellow_friend_add():
    try:
        message = APIAdmin.process("add", request.json)
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/friend/<key>", methods=["DELETE"])
def yellow_friend_block(key):
    try:
        message = APIAdmin.process("block", key)
        return jsonify(message), 200
    except:
        return processFail(), 400


@app.route("/api/chat_room/<key>", methods=["DELETE"])
def yellow_exit(key):
    try:
        message = APIAdmin.process("exit", key)
        return jsonify(message), 200
    except:
        return processFail(), 400
