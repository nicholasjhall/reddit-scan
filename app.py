from flask import Flask, redirect, url_for, render_template, request, jsonify, json
import praw
import nltk
# nltk.download('punkt') is needed

app = Flask(__name__)
#app.config('JSON_SORT_KEYS') = False
reddit = praw.Reddit("scanner")
karma_dict = {}
valid_tags = ['JJ','NN','NNS','VBZ','VBN','VBD','VBP','VB','NNP']
# IDEA: keep track of not only the total karma, but also the avg karma per word, by dividing by the number of appearances


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
		for submission in subreddit.top(limit=5):
			print(submission.title)
			words = nltk.word_tokenize(submission.title)
			tagged = nltk.pos_tag(words)
			for word in tagged:
				if word[1] in valid_tags:
					if word[0] in karma_dict:
						karma_dict[word[0]] += submission.score
					else:
						karma_dict[word[0]] = submission.score
		print(karma_dict)
		return render_template("subreddit.html", sub=sub)
	else:
		return render_template("subreddit.html", sub=sub)

@app.route("/data")
def data():
	karma_dict_sorted = {k: v for k, v in sorted(karma_dict.items(), key=lambda item: item[1])}
	response = app.response_class(json.dumps(karma_dict_sorted, sort_keys=False), mimetype=app.config['JSONIFY_MIMETYPE'])
	return response



if __name__ == "__main__":
	app.run(debug = True)