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
            mode = request.form["mode"]

            if mode == "premium":
                prompt = f"""
You are an expert short-form content strategist.

Generate ONLY 3 premium hooks.

Niche: {niche}
Goal: {goal}
Platform: {platform}
Hook Type: {hook_type}

For each hook provide:

1. Hook
2. Why it works
3. Best use case

Make every hook unique and high quality.
"""
                max_tokens = 500

            else:
                prompt = f"""
Generate 7 additional hooks.

Niche: {niche}
Goal: {goal}
Platform: {platform}
Hook Type: {hook_type}

Rules:
- Keep hooks under 15 words.
- Make them highly engaging.
- Number them from 1 to 7.
"""
                max_tokens = 250

            response = client.chat.completions.create(
                model="meta/llama-3.3-70b-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=0.7
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
