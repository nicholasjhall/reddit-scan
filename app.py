from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
	if request.method == "POST":
		sub = request.form["sub"]
		return redirect(url_for("subredditPage", sub=sub))
	else:
		return render_template("index.html")


@app.route("/<sub>", methods=["POST", "GET"])
def subredditPage(sub):
	return render_template("subreddit.html", sub=sub)


if __name__ == "__main__":
	app.run(debug = True)