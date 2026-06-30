import os
import traceback
from flask import Flask
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("Meta"),
    timeout=15
)

@app.route("/")
def home():
    return '<a href="/test">Test AI</a>'

@app.route("/test")
def test():
    try:
        models = client.models.list()
        return f"<pre>{models}</pre>"
    except Exception:
        return f"<pre>{traceback.format_exc()}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
