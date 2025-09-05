# from flask import request, jsonify
# from bson import ObjectId
# from db import mongo 
# from app import app
# from flask import Flask, render_template, request, redirect, url_for


# @app.route('/api/update-property/<property_id>', methods=['PUT'])
# def update_property(property_id):
#     try:
#         # Get updated data from request
#         updated_data = request.get_json()
        
#         # Convert string ID to ObjectId
#         obj_id = ObjectId(property_id)
        
#         # Update the property in the database
#         result = mongo.db.properties.update_one(
#             {'_id': obj_id},
#             {'$set': updated_data}
#         )
        
#         if result.modified_count > 0:
#             return jsonify({
#                 'status': 'success',
#                 'message': 'Property updated successfully'
#             })
#         else:
#             return jsonify({
#                 'status': 'error',
#                 'message': 'No changes made or property not found'
#             }), 404
            
#     except Exception as e:
#         return jsonify({
#             'status': 'error',
#             'message': str(e)
#         }), 500
        


# @app.route("/edit-property/<property_id>")
# def edit_property(property_id):
#     try:
#         # Convert string ID to ObjectId
#         obj_id = ObjectId(property_id)
#         property_data = mongo.db.properties.find_one({"_id": obj_id})
#         # property_data = mongo.properties.find_one({'_id': obj_id})
        
#         if property_data:
#             # Convert ObjectId to string for JSON serialization
#             property_data['_id'] = str(property_data['_id'])
#             return render_template("edit_property.html", property=property_data)
#         else:
#             return render_template("error.html", error="Property not found"), 404
            
#     except Exception as e:
#         return render_template("error.html", error=str(e)), 500



from flask import request, jsonify, render_template
from bson import ObjectId
from db import mongo
from app import app


# @app.route('/api/update-property/<property_id>', methods=['PUT'])
# def update_property(property_id):
#     try:
#         updated_data = request.get_json()
#         obj_id = ObjectId(property_id)

#         result = mongo.db.properties.update_one(
#             {"_id": obj_id},
#             {"$set": updated_data}
#         )

#         if result.modified_count > 0:
#             return jsonify({"status": "success", "message": "Property updated successfully"})
#         else:
#             return jsonify({"status": "error", "message": "No changes made or property not found"}), 404

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/update-property/<property_id>", methods=["PUT"])
def update_property(property_id):
    try:
        data = request.json
        mongo.db.properties.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": data}
        )
        return jsonify({"status": "success", "message": "Property updated"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/edit-property/<property_id>")
def edit_property(property_id):
    try:
        obj_id = ObjectId(property_id)
        property_data = mongo.db.properties.find_one({"_id": obj_id})

        if property_data:
            property_data["_id"] = str(property_data["_id"])
            return render_template("edit_property.html", property=property_data)
        else:
            return render_template("error.html", error="Property not found"), 404

    except Exception as e:
        return render_template("error.html", error=str(e)), 500
