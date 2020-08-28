Subject Scan creates a graph of the top 20 title words by karma per occurrence, with one-off popular words and unimportant parts of speech removed. The data is taken from the all time top 500 posts of the specified subreddit.
The algorithm used is: 
1. Collect total karma and occurrences for each word in the titles, checking if the word is a valid part of speech
2. Find average karma per occurrence for each word
3. Remove words from the graph if they share the exact same average karma per occurrence as any other words