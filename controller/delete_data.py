from flask import request , jsonify
from bson import ObjectId
from model.DataBase_model import delete_json
from app import app

@app.route("/api/delete-property/<property_id>", methods=["DELETE"])
def delete_property(property_id):
    try:
        result = delete_json({"_id": ObjectId(property_id)}, collection_name="properties")
        if result.deleted_count == 1:
            return jsonify({"status": "success", "message": "Property deleted successfully"})
        else:
            return jsonify({"status": "error", "message": "Property not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
