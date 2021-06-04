from flask import Flask,render_template
import cv2

app=Flask(__name__)

@app.route('/')
def index():
    outname=detect('static/101.png')
    return render_template('face.html',outname=outname)

def detect(filename):
    face_cascade = cv2.CascadeClassifier('/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml')

    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    outname='static/face.png'
    cv2.imwrite(outname,img)
    return outname


if __name__=='__main__':
    app.run()