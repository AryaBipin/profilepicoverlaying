from email.mime import image
from imp import reload
from operator import contains
from pathlib import Path
from flask import Flask, redirect,request,render_template,flash,url_for,send_from_directory
import urllib.request
import os
from werkzeug.utils import secure_filename
from PIL import Image,ImageDraw
import pyodbc
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from urllib import parse
import datetime

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secretkey'          
UPLOAD_FOLDER = 'static/uploads'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def home():
    m = 6
    count = 0
    src_or="static/uploads/profile"
    file_list1=os.listdir(src_or)
    coun=len(file_list1)
    src_dir = "static/uploads/original/"
    count=len(os.listdir(src_dir))
    #print(count)
    file_list = os.listdir(src_dir)
    file_paths=[]
    j=1
    for i in range(m):
        a = file_list[count-j]
        file_paths.append(a)
        j+=1
    return render_template('index.html',file_paths=file_paths,file_list1=file_list1,coun=coun)
 

@app.route("/upload", methods=['GET','POST'])
def upload_image():
    file = request.files['image']
    file.save('static/uploads/original/'+(datetime.datetime.now()).strftime("%m%d%y,%H%M%S")+'filename.jpg')
    img = Image.open(r"static/uploads/Adlogo2.png")
    background = Image.open(r"static/uploads/original/"+(datetime.datetime.now()).strftime("%m%d%y,%H%M%S")+"filename.jpg")
    background.paste(img, (0, 0), img)
    mask = Image.new('L', background.size)
    mask_draw = ImageDraw.Draw(mask)
    width, height = background.size
    mask_draw.ellipse((5, 5, width, height), fill=255)
    background.putalpha(mask)
    background.save('static/uploads/profile/'+(datetime.datetime.now()).strftime("%m%d%y,%H%M%S")+'profile.png')
    return redirect(url_for('home'))
if __name__ == "__main__":
    app.run(debug=True)