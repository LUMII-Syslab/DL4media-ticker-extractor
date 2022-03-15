import os, json
from flask import Flask, request

from tickerExtractor import extract_text

app = Flask(__name__)
app.config["SECRET_KEY"] = "model!"


@app.route('/')
def get_index():
	return "Server for model is running"


@app.route('/extract-ticker', methods=["POST"])
def extract_ticker():
	file = request.files.getlist("file")
	# source_img = misc.imread(io.BytesIO(source[0].read()))

	result = extract_text(file)
	
	return result


if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', threaded=True)
