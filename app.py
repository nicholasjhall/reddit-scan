from flask import Flask, redirect, url_for, render_template, request, jsonify, json
import praw
import nltk
import numpy as np
# nltk.download('punkt') is needed

app = Flask(__name__)
reddit = praw.Reddit("scanner")
karma = {}
occurrences = {}
valid_tags = ['JJ','NN','NNS','VBZ','VBN','VBD','VBP','VB','NNP']


@app.route("/", methods=["POST", "GET"])
def home():
	if request.method == "POST":
		sub = request.form["sub"]
		return redirect(url_for("subredditPage", sub=sub))
	else:
		return render_template("index.html")


@app.route("/<sub>", methods=["POST", "GET"])
def subredditPage(sub):
	global karma
	global occurrences

	if request.method == "GET":
		subreddit = reddit.subreddit(sub)
		
		# iterate through top 500 posts to tokenize and tag words
		for submission in subreddit.top(limit=500):
			words = nltk.word_tokenize(submission.title)
			tagged = nltk.pos_tag(words)

			# iterate through tagged words to clean and sum karma
			for fullWord in tagged:
				word = [fullWord[0].lower(), fullWord[1]]
				# only use word if it is a valid part of speech
				if word[0].isalpha() and word[1] in valid_tags:
					if word[0] in karma:
						karma[word[0]] += submission.score
						occurrences[word[0]] += 1
					else:
						karma[word[0]] = submission.score
						occurrences[word[0]] = 1
		return render_template("subreddit.html", sub=sub)
	else:
		# reset total karma and occurrences for new subreddit
		karma = {}
		occurrences = {}
		newSub = request.form["sub"]
		return redirect(url_for("subredditPage", sub=newSub))

@app.route("/data")
def data():
	# change total karma dict to karma per occurrence dict
	for word in karma:
		karma[word] /= occurrences[word]
	karmaNoDup = {}
	karmaValues = list(karma.values())
	# eliminate all words with duplicate values
	for key, value in karma.items():
		valueCount = karmaValues.count(value)
		if valueCount == 1:
			karmaNoDup[key] = value
	# sort words by karma per occurrence in descending order
	karma_dict_sorted = {k: v for k, v in sorted(karmaNoDup.items(), reverse=True, key=lambda item: item[1])}
	# convert dictionary to json
	response = app.response_class(json.dumps(karma_dict_sorted, sort_keys=False), mimetype=app.config['JSONIFY_MIMETYPE'])
	return response



if __name__ == "__main__":
	app.run(debug = True)