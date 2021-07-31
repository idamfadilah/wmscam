from flask import Flask, render_template, request
import base64
import numpy as np
import cv2 as cv

app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        print(request.form['source'])
        print(request.form['target'])
        convert_and_save(request.form['source'], "source")
        convert_and_save(request.form['target'], "target")
        changetogray()
        return render_template('indax.html')
    return render_template('index.html')

def convert_and_save(b64_string, name):
    b64_string  = b64_string.split(',')
    with open(name+".jpeg", "wb") as fh:
        fh.write(base64.decodebytes(b64_string[1].encode()))

def changetogray():
    path = r'source.jpeg'
    img_rgb = cv.imread(path)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

    template = cv.imread('target.jpeg' ,0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    i = 0
    for pt in zip(*loc[::-1]):
        i+=1
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        cv.imwrite("static/dungser.jpeg",img_rgb)
