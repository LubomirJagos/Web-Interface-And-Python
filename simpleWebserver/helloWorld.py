import os
import numpy as np
import subprocess
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import csv
import sys

import time
import datetime
from shutil import copyfile
import shutil

#from oct2py import octave
#octave.addpath('/home/lubo/Documents/Otcave')

from flask import Flask, request

currDir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_url_path='/static')
@app.route('/')
def index():
	indexFile = open(os.path.dirname(os.path.abspath(__file__)) + "/index.html")
	return indexFile.read()

@app.route('/calc')
def calc():
	indexFile = open(os.path.dirname(os.path.abspath(__file__)) + "/calc.html")
	return indexFile.read()

@app.route('/resultForm1', methods=["GET"])
def deg2rad():
	data = request.args.get('degInput')
	returnMsg = "User input degrees to radians: " + str(np.deg2rad(int(data)))
	#returnMsg += "<br /><a href='/'>&lt;Back</a>"
	return returnMsg

@app.route('/showScope')
def showScope():
	f = open(os.path.dirname(os.path.abspath(__file__)) + "/showScope.html")
	return f.read()

@app.route('/oscilloscope', methods=['GET'])
def readHantek6022():
	timeToRead = request.args.get('timeToRead')
	if (timeToRead is None):
		timeToRead = 0.001
	sampleRate = request.args.get('sampleRate')
	if (sampleRate is None):
		sampleRate = 20

	#scopeData = subprocess.check_output(['capture_6022.py','-t '+str(timeToRead), '-r '+str(sampleRate)])	
	scopeData = subprocess.check_output(['capture_6022.py','-t '+str(timeToRead)])	

	f = open("captured_data.csv", "w")
	f.write(str(scopeData, 'utf-8'))	# <----- CONVERT b' BYTES STREAM INTO STRING FROM SUBPROCESS!
	f.close()

	x = []
	y = []
	with open('captured_data.csv','r') as csvfile:
		plots = csv.reader(csvfile, delimiter=',')
		for row in plots:
			x.append(float(row[0]))
			y.append(float(row[1]))

	
	plt.clf()
	plt.plot(x,y, label='LuboJGraph')
	figname = ''.join([currDir + '/static/captured_image.png'])
	plt.savefig(figname)
	
	return scopeData
	
@app.route('/octave-deg-2-rad')
def octaveDeg2Rad():
	headerResult = ""
	#headerResult += "Time (ms): " + str(int(round(time.time())))
	headerResult += "Time (ms): " + str(int(round(time.time_ns()//1000000)))

	filePath = '/tmp/_python_octave'
	if not os.path.isdir(filePath):
		os.mkdir(filePath)

	#remove file if it were there previosly copied
	filePath = '/tmp/_python_octave/deg2rad.m'
	if os.path.exists(filePath):
		os.remove(filePath)

	#remove file if there were already copied before
	filePath = '/tmp/_python_octave/deg2rad.sh'
	if os.path.exists(filePath):
		os.remove(filePath)

	# function shutil.copyfile is not copying metadata
	#THIS IS RIGHT ALEO COPYING PERMISSIONS TO BE RUNNABLE
	#    copying files to /tmp/_python_octave dir to be executable python.flask
	#    process user (do this to be sure files are in dir where they will be runnable)
	shutil.copy2(currDir+'/deg2rad.m', '/tmp/_python_octave/deg2rad.m')
	shutil.copy2(currDir+'/deg2rad.m', '/tmp/_python_octave/deg2rad.sh')

	#octaveResult = subprocess.check_output([currDir+'/deg2rad.sh'])
	octaveResult = subprocess.check_output(['/tmp/_python_octave/deg2rad.sh'])
	#octaveResult = subprocess.check_output(['bash','-c','octave-cli','/tmp/deg2rad.m'])

	footerResult = ""
	footerResult += "Time (ms): " + str(int(round(time.time_ns()//1000000)))

	outputStr =  headerResult
	outputStr += "<br />"
	outputStr += str(octaveResult, 'utf-8')
	outputStr += "<br />"
	outputStr += footerResult
	return outputStr

@app.route('/makeCamera')
def makecamera():
	filePath = '/tmp/camera'
	if not os.path.isdir(filePath):
		os.mkdir(filePath)
	result = subprocess.check_output(['fswebcam',currDir+'/static/CameraCurrPic.jpg'])
	return 'camera image captured'

@app.route('/showCamera')
def showCamera():
	indexFile = open(currDir + "/showCamera.html")
	return indexFile.read()

if __name__ == '__main__':
	app.run(debug=True, port=80, host='0.0.0.0')

