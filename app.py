import os
import traceback
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("Meta")
)

@app.route("/", methods=["GET", "POST"])
def home():
    hooks = ""

    if request.method == "POST":
        try:
            niche = request.form["niche"]
            goal = request.form["goal"]
            platform = request.form["platform"]
            hook_type = request.form["hook_type"]

            prompt = f"""
Generate 3 premium hooks.

Niche: {niche}
Goal: {goal}
Platform: {platform}
Hook Type: {hook_type}

For each hook provide:
1. Hook
2. Why it works
3. Best use case.
"""

            response = client.chat.completions.create(
                model="meta/llama-3.3-70b-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )

            hooks = response.choices[0].message.content

        except Exception:
            return f"<pre>{traceback.format_exc()}</pre>"

    return render_template(
        "index.html",
        hooks=hooks
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
