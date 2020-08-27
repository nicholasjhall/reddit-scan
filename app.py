from flask import Flask, redirect, url_for, render_template, request
import praw
import nltk
# nltk.download('punkt') is needed

app = Flask(__name__)
reddit = praw.Reddit("scanner")
karma_dict = {}


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
		for submission in subreddit.top(limit=50):
			print(submission.title)
			words = nltk.word_tokenize(submission.title)
			karma = submission.score
			tagged = nltk.pos_tag(words)
			for word in tagged:
				if word in karma_dict:
					karma_dict[word] += submission.score
				else:
					karma_dict[word] = submission.score
		print(karma_dict)
		return render_template("subreddit.html", sub=sub)
	else:
		return render_template("subreddit.html", sub=sub)


if __name__ == "__main__":
	app.run(debug = True)