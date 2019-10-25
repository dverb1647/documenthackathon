import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory

app = Flask("image_scanning")
folder = 'data'
app.config['UPLOAD_FOLDER'] = folder

@app.route('/', methods=['GET', "POST"])
def uploadFileForScanning():
    if request.method == 'POST':
        file = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        return send_from_directory(app.config['UPLOAD_FOLDER'], file.filename)
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''
if __name__ == "__main__":
    app.run()