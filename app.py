from flask import Flask, redirect, url_for, render_template, request
import praw
app = Flask(__name__)
reddit = praw.Reddit("scanner")


@app.route("/", methods=["POST", "GET"])
def home():
	print("console test")
	if request.method == "POST":
		sub = request.form["sub"]
		return redirect(url_for("subredditPage", sub=sub))
	else:
		print("Base home page")
		return render_template("index.html")


@app.route("/<sub>", methods=["POST", "GET"])
def subredditPage(sub):
	if request.method == "GET":
		print(sub)
		subreddit = reddit.subreddit(sub)
		for submission in subreddit.hot(limit=1):
			print(submission.title)
		return render_template("subreddit.html", sub=sub)
	else:
		return render_template("subreddit.html", sub=sub)


if __name__ == "__main__":
	app.run(debug = True)