import os
import numpy as np

from flask import Flask, request


currDir = os.path.abspath(__file__)

app = Flask(__name__)
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

if __name__ == '__main__':
	app.run(debug=True, port=80, host='0.0.0.0')

