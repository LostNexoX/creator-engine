from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return "POST received successfully!"
    return """
    <form method="POST">
        <button type="submit">Test Button</button>
    </form>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
