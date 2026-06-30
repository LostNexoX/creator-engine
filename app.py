import os
from flask import Flask
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("Meta"),
    timeout=10
)

@app.route("/")
def home():
    return '<a href="/test">Test AI</a>'

@app.route("/test")
def test():
    try:
        return "Before API call..."
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
