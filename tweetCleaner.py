import json
import sys
import re
from nltk.corpus import stopwords
stop_words = list(stopwords.words('english'))
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
letters = 'abcdefghijklmnopqrstuvwxyz'



class TweetCleaner:
	def __init__(self):
		self.validTweets = []
		self.validRetweets = []

		self.letters = 'abcdefghijklmnopqrstuvwxyz'
		self.valid = 'abcdefghijklmnopqrstuvwxyz@#1234567890%$.'

		self.regexList = ['^.?https://','^.?&amp;','\.\.\.$', '\.{1,}?$', '^\.{1,}?' ]
		self.stop_words = list(stopwords.words('english'))
# Takes in a FILE, returns 2 lists, validTweets and validRetweets
def cleanTweets(file):
	# This function grabs tweets from a json file and cleans them. leaves lower case chars and numbers along with a few key punctuation characters
	# Only cleans/formats tweets, drops any links. 
	validTweets = []
	validRetweets = []
	regex = '^.?https://'
	regex2 = '^.?&amp;'
	regex3 = '\.\.\.$'
	regex4 = '\.{1,}?$'
	regex5 = '^\.{1,}?'
	porterStemmer = PorterStemmer()
	snowballStemmer = SnowballStemmer('english')
	with open(file, encoding='utf8') as f:
		
		data = json.load(f)
		valid = 'abcdefghijklmnopqrstuvwxyz@#1234567890%$.'
		#redundant but easier
		for tweet in data:
			t = tweet['text'].lower()
			t = t.split('\n')
			aTweet = []
			tweetData = {}
			
			for subtweet in t:
				
				for word in subtweet.split(' '):
					
					if not re.match(regex, word) and not re.match(regex2, word) and not re.match(regex3, word):
						
						if word == 'rt':
							#checking if is_retweet exists in the tweet
							try:
								tweetData['is_retweet'] = tweet['is_retweet']
							except:
								tweet['is_retweet'] = True

						if word != '' and word != ' ' and word != 'rt':
							if len(word) > 2:
								if word[len(word)-1] == 's' and word[len(word) - 2] =="'":
									word = word[:len(word)-2]
							fixedWord = ''
							for char in word:
								if char in valid:
									fixedWord += char
							if fixedWord != '':
								if len(fixedWord) > 1:
									if checkRandomInt(fixedWord):
										#need to deal with . at end of sentence, otherwise HELLO. != HELLO
										if len(fixedWord) >=2:
											if '.' in word:
												fixedWord = removePeriods(fixedWord)
										
										fixedWord = porterStemmer.stem(fixedWord)
										fixedWord = snowballStemmer.stem(fixedWord)
										if fixedWord != '':
											aTweet.append(fixedWord)
			#for later
			tweetData['source'] = tweet['source']
			try:
				tweetData['is_retweet'] = tweet['is_retweet']
			except:
				tweetData['is_retweet'] = False

			tweetData['text'] = aTweet
			tweetData['created_at'] = tweet['created_at']
			
			if len(aTweet) != 0:
				if tweetData['is_retweet']:
					validRetweets.append(tweetData)
				else:
					validTweets.append(tweetData)
			
	return validTweets, validRetweets

def removePeriods(word):
	fixedWord = ''
	if (word[-1] == '.' and word [-2] in letters) or (word[0] == '.' and word[1] in letters):
		for char in word:
			if char != '.':
				fixedWord += char
	return fixedWord


# Takes in a 'tweet' and returns its text content as ngrams of length N
# tweet == list, N == int, removeAllStopwords == T/F
def createNgrams(tweet, N, removeAllStopwords):
	# ngrams should be restricted to being <= 5 as tweets do not have many words. 
	# N = 2 or 3 should give the most accurate results

	
	tweetLength = len(tweet)
	
	if N > tweetLength:
		# If an input tweet is less than the requested ngram length 
		return None

	# Cleaning a tweet is insignficant, only fix efficiency if it runs too slow
	cleanedTkns = []
	for token in tweet:
		tkn = checkStopWords(token)
		print(token, tkn)
		if tkn != None:
			cleanedTkns.append(tkn)

	if N == 1:
		return cleanedTkns

	else:

		if removeAllStopwords:
			tokens = cleanedTkns

		else:
			tokens = tweet
	
		ngrams = []
		for i in range( len(tokens) - N+1 ):
			ngram = tokens[i: i+N]

			print('ngram:' , ngram, 'From:', i, 'To:', i+N-1)
			# ngram = checkStopWords(ngram)
			
			# if ngram != None:
			ngrams.append(ngram)
		
		if len(ngrams) != 0:
			return ngrams


# This function takes in a "word" and returns True or False if its a year or a number
# Numbers can be ignored where years carry significance
def checkRandomInt(word):
	try: 
		word = float(word)
		if word < 1500 or word > 2200:
			return False
		else:
			return True
	except:
		return True


def checkStopWords(gram):
	#currently removes an ngram if all of the grams are stopwords 
	if gram in stop_words:
		return None
	else:
		return gram
	

def main():
	FILENAME = 'Ttweets.json'
	tweets, retweets = cleanTweets(FILENAME)
	print('Total Tweets:',len(tweets))
	print('Total Retweets:', len(retweets))
	for tweet in tweets:
		print(createNgrams(tweet['text'], 2, True))
		input()





if __name__ == '__main__':
	main()