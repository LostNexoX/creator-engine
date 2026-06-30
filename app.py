import os
import traceback
from flask import Flask
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("Meta"),
    timeout=20
)

@app.route("/")
def home():
    return """
    <h1>AI Test</h1>
    <form method="POST" action="/test">
        <button type="submit">Test AI</button>
    </form>
    """

@app.route("/test", methods=["POST"])
def test():
    try:
        response = client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",
            messages=[
                {
                    "role": "user",
                    "content": "Reply with only the word Hello"
                }
            ],
            max_tokens=10
        )

        return f"<h2>{response.choices[0].message.content}</h2>"

    except Exception:
        return f"<pre>{traceback.format_exc()}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
