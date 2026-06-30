from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>AI Test</h1>
    <a href="/test">Click Me</a>
    """

@app.route("/test")
def test():
    return "TEST ROUTE WORKING"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
