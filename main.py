from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os, sys, subprocess, imghdr

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.mp4', '.mov', '.avi']
app.config['UPLOAD_PATH'] = 'uploads'

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'mp4' else 'MP4')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

UPLOAD_FILE=os.getcwd()+'/static/'
vids = {}

def get_vids():
    global vids
    for i in os.listdir(UPLOAD_FILE):
        if i.endswith('.mp4'):
            name = i.split('.')[0]
            vids[name]=i

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
   get_vids()
   if request.method == 'POST':
      f = request.files['file']
      ext = f.filename.split('.')[1]
      name = request.form.get("title")
      result = subprocess.run(['ipfs', 'add', UPLOAD_FILE+f.filename], stdout=subprocess.PIPE)
      res = result.stdout.decode("utf-8")
      res = res.split(' ')[1]

      fi=open('hashes.txt', 'a')
      fi.write(res)
      fi.write('\n')
      fi.close()
      f.save((UPLOAD_FILE+str(name)+'.'+ext))
      get_vids()
      return render_template('index.html', videos=vids)
   else:
        #print(vids_, file=sys.stderr)
      return render_template('index.html', videos=vids)

# @app.route("/")
# def hello_world():
#     get_vids()
#     #print(vids_, file=sys.stderr)
#     return render_template('index.html', videos=vids)

if __name__ == "__main__":
    app.run(port='8000')
