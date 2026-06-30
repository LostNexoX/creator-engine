from flask import Flask, request
import os
import traceback
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("Meta")
)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            response = client.chat.completions.create(
                model="meta/llama-3.3-70b-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": "Say hello."
                    }
                ],
                max_tokens=20
            )

            return response.choices[0].message.content

        except Exception:
            return f"<pre>{traceback.format_exc()}</pre>"

    return """
    <h1>AI Test</h1>
    <form method="POST">
        <button type="submit">Test AI</button>
    </form>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
