from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import os
import time
import tempfile
from db import init_db
import time

from werkzeug.utils import secure_filename
app = Flask(__name__)

mongo = init_db(app)

from controller import *





app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

@app.route("/", methods=['GET', 'POST'])
def home():
    print("its working")
    # if request.method == 'POST':
    #     if 'file' not in request.files:
    #         return redirect(request.url)
    #     file = request.files['file']
    #     if file.filename == '':
    #         return redirect(request.url)
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         return redirect(url_for('home'))
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)) , debug=True)


# # docker run -p 5000:5000 automation


