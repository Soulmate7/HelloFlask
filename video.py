#!/usr/bin/env python3
from flask import Flask, render_template, request
import cv2
import subprocess

image_save='./imgs'
app=Flask(__name__)
@app.route('/')
def index():
    video_path=request.args.get("video_path",type=str)
    # if outname == None:
    #     outname='static/basketball.mp4'
    return render_template('video.html',outname=video_path)

@app.route('/cut')
def cut():
    cap = cv2.VideoCapture(video_path)
    video_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    for i in range(int(video_frame_count)):
        _, img = cap.read()
        #高斯模糊+边缘检测
        img = cv2.GaussianBlur(img, (3, 3), 0)
        canny = cv2.Canny(img, 50, 150)
        cv2.imwrite(('static/imgs/image{}.jpg').format(i),canny)
        
        #cv2.imshow('img', canny)
        #cv2.waitKey(int(1000/24))
    return render_template('aftercut.html',video_frame_count=video_frame_count,firstframe='static/imgs/image0.jpg')

@app.route('/merge')
def merge():
    cap = cv2.VideoCapture(video_path)
    video_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter('static/imgs/output.mp4', fourcc, 24.0, size)

    for i in range(int(video_frame_count)):
        img = cv2.imread(('static/imgs/image{}.jpg').format(i))
        out.write(img)
    out.release()
    return render_template('merge.html',output='static/imgs/output.mp4')


if __name__=='__main__':
    video_path='static/basketball.mp4'
    app.run(debug=True)
