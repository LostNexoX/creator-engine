from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

@app.route("/", methods=["GET", "POST"])
def home():
    hooks = ""

    if request.method == "POST":
        niche = request.form["niche"]
        goal = request.form["goal"]

        prompt = f"""
You are an expert short-form content strategist.

Generate 10 highly engaging hooks.

Niche: {niche}
Goal: {goal}

Rules:
- Avoid generic hooks.
- Keep each hook under 15 words.
- Suitable for Instagram Reels and TikTok.
- Curiosity-driven and specific.
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

    return render_template(
        "index.html",
        hooks=hooks
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
