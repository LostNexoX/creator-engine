import os
import json
import traceback
from datetime import datetime
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("Meta")
)


def load_history():
    try:
        with open("history.json", "r") as f:
            return json.load(f)
    except:
        return []


def save_history(item):
    try:
        history = load_history()
        history.insert(0, item)
        history = history[:20]

        with open("history.json", "w") as f:
            json.dump(history, f, indent=2)
    except:
        pass


@app.route("/", methods=["GET", "POST"])
def home():
    hooks = ""
    script = ""
    error = ""

    try:
        if request.method == "POST":

            action = request.form.get("action")

            if action == "hooks":

                niche = request.form["niche"]
                goal = request.form["goal"]
                platform = request.form["platform"]
                hook_type = request.form["hook_type"]
                mode = request.form["mode"]

                if mode == "premium":
                    prompt = f"""
Generate ONLY 3 premium hooks.

Niche: {niche}
Goal: {goal}
Platform: {platform}
Hook Type: {hook_type}

For each hook provide:
1. Hook
2. Why it works
3. Best use case.
"""
                    max_tokens = 500

                else:
                    prompt = f"""
Generate 7 additional hooks.

Niche: {niche}
Goal: {goal}
Platform: {platform}
Hook Type: {hook_type}

Number each hook from 1 to 7.
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

                save_history({
                    "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                    "niche": niche,
                    "goal": goal,
                    "platform": platform,
                    "hook_type": hook_type,
                    "hooks": hooks
                })

            elif action == "script":

                selected_hook = request.form["selected_hook"]

                prompt = f"""
Write a highly engaging 30-second short video script.

Hook:
{selected_hook}

Requirements:
- Conversational
- Strong payoff
- Suitable for Instagram Reels and TikTok
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

                script = response.choices[0].message.content

    except Exception:
        return f"<pre>{traceback.format_exc()}</pre>"

    history = load_history()

    return render_template(
        "index.html",
        hooks=hooks,
        script=script,
        error=error,
        history=history
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
