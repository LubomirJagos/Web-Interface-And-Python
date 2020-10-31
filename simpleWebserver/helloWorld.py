import os
import numpy as np
import subprocess
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import csv
import sys

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
	f.write(str(scopeData, 'utf-8'))
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
	



if __name__ == '__main__':
	app.run(debug=True, port=80, host='0.0.0.0')

