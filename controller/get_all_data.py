from flask import jsonify, render_template
from model.DataBase_model import get_all_json
from app import app

# Add this route to your app.py
@app.route("/api/data")
def get_all_data():
    try:
        # Get all data from the properties collection
        properties = get_all_json(collection_name="properties")
        return jsonify({
            "status": "success",
            "count": len(properties),
            "data": properties
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



# Add this route to display the data in a HTML table
@app.route("/view-data")
def view_data():
    try:

        properties = get_all_json(collection_name="properties")
        print("this is the properties = = " , properties)
        return render_template("data_table.html", properties=properties)
    except Exception as e:
        return render_template("error.html", error=str(e))