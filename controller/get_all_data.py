# from flask import jsonify, render_template
# from model.DataBase_model import get_all_json
# from app import app

# # Add this route to your app.py
# @app.route("/api/data")
# def get_all_data():
#     try:
#         # Get all data from the properties collection
#         properties = get_all_json(collection_name="properties")
#         return jsonify({
#             "status": "success",
#             "count": len(properties),
#             "data": properties
#         })
#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500



# # Add this route to display the data in a HTML table
# @app.route("/view-data")
# def view_data():
#     try:

#         properties = get_all_json(collection_name="properties")
#         print("this is the properties = = " , properties)
#         return render_template("data_table.html", properties=properties)
#     except Exception as e:
#         return render_template("error.html", error=str(e))




from flask import request, jsonify, render_template
from model.DataBase_model import get_all_json, get_filtered_properties
from app import app
import math

@app.route("/api/data")
def get_all_data():
    try:
        # Get pagination and search parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        # Get filtered and paginated data
        properties, total_count = get_filtered_properties(
            collection_name="properties",
            search=search,
            page=page,
            per_page=per_page
        )
        
        # Calculate total pages
        total_pages = math.ceil(total_count / per_page) if per_page > 0 else 1
        
        return jsonify({
            "status": "success",
            "count": len(properties),
            "total_count": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "data": properties
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/view-data")
def view_data():
    try:
        # Get query parameters for initial page load
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        # Get filtered and paginated data
        properties, total_count = get_filtered_properties(
            collection_name="properties",
            search=search,
            page=page,
            per_page=per_page
        )
        
        # Calculate total pages
        total_pages = math.ceil(total_count / per_page) if per_page > 0 else 1
        
        return render_template(
            "data_table.html", 
            properties=properties,
            current_page=page,
            per_page=per_page,
            total_pages=total_pages,
            total_count=total_count,
            search=search
        )
    except Exception as e:
        return render_template("error.html", error=str(e))