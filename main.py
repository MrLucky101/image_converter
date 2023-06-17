from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import cv2
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"The operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    if operation == "webp":
        newFilename = f"static/{filename.split('.')[0]}.webp"
        cv2.imwrite(newFilename, img)
        return newFilename
    elif operation == "png":
        newFilename = f"static/{filename.split('.')[0]}.png"
        cv2.imwrite(newFilename, img)
        return newFilename
    elif operation == "jpg":
        newFilename = f"static/{filename.split('.')[0]}.jpg"
        cv2.imwrite(newFilename, img)
        return newFilename
        

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation") 
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your Image has been processed and available <a href= '/{new}' target ='_blank' >here </a>")
            return render_template("index.html")
        
    return render_template("index.html")
app.run(debug=True)

