import os
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
    error = ""

    if request.method == "POST":
        try:
            niche = request.form["niche"]
            goal = request.form["goal"]
            platform = request.form["platform"]
            hook_type = request.form["hook_type"]

            prompt = f"""
You are an expert short-form content strategist.

Generate 10 highly engaging hooks.

Niche: {niche}
Goal: {goal}
Platform: {platform}
Hook Type: {hook_type}

Rules:
- Avoid generic hooks.
- Keep each hook under 15 words.
- Suitable for the selected platform.
- Match the selected hook type strongly.
- Number each hook from 1 to 10.
"""

            response = client.chat.completions.create(
                model="meta/llama-3.3-70b-instruct",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.8
            )

            hooks = response.choices[0].message.content

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        hooks=hooks,
        error=error
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
