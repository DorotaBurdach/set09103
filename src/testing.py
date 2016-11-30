from flask import Flask
app = Flask(__name__)

@app.route('/')
def root():
  return "This is a test for the connection:Passed", 400

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)