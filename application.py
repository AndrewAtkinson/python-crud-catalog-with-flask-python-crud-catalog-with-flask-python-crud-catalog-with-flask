from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!!"

@app.route("/setup")
def setup():
    return "Hello World!!"

if __name__ == "__main__":
	''' Run the web server on all external ports (we need this for the vagrant machine)
		and on port 8000. debugging for now is allowed so changes can be tested quickly
		and we can see any error messages.
	'''
    app.run(host='0.0.0.0', port=8000, debug=True)