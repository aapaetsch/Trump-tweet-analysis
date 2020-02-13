import json 
import sys
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

stop_words = list(stopwords.words('english'))
letters = 'abcdefghijklmnopqrstuvwxyz'

class TweetCleaner:

	def __init__(self):
		self.validTweets = []
		self.validRetweets = []

		self.letters = 'abcdefghijklmnopqrstuvwxyz'
		self.valid = 'abcdefghijklmnopqrstuvwxyz@#1234567890%$.'
		self.ints = '1234567890'

		self.regexList = ['^.?https://','^.?&amp;','\.\.\.$', '\.{1,}?$', '^\.{1,}?' ]
		self.stop_words = list(stopwords.words('english'))


	def cleanTweets(self, file):
		# This method grabs tweets from a json file and cleans them. leaves lower case chars and numbers along with a few key punctuation characters
		# Only cleans/formats tweets, drops any links. 
		porterStemmer = PorterStemmer()
		snowballStemmer = SnowballStemmer('english')

		with open(file, encoding='utf8') as f:

			data = json.load(f)

			for tweet in data:
				
				t = tweet['text'].lower()
				t = t.split('\n')
				aTweet = []
				tweetData = {}

				for subtweet in t:
					for word in subtweet.split(' '):
						if not re.match(self.regexList[0], word):
							if not re.match(self.regexList[1], word):
								if not re.match(self.regexList[2], word):

									if word not in ['', ' ', 'rt']:
										fixedWord = ''
										for char in word:
											if char in valid:
												fixedWord += char
										if fixedWord != '':
											if len(fixedWord) > 1:
												if self.__checkRandomInt(fixedWord):
													if len(fixedWord) >= 2 and '.' in word:
														fixedWord = self.__removePeriods(fixedWord)

											fixedWord = porterStemmer.stem(fixedWord)
											fixedWord = snowballStemmer.stem(fixedWord)
											if len(fixedWord) > 2 and fixedWord[len(fixedWord)-1] == 's' and fixedWord[len(fixedWord)-2] == "'":
												fixedWord = fixedWord[:len(fixedWord)-2]
											if fixedWord != '':
												aTweet.append(fixedWord)

									if word == 'rt':
										try:
											tweetData['is_retweet'] = tweet['is_retweet']
										except:
											tweet['is_retweet'] = True
					
					tweetData['source'] = tweet['source']
					try:
						tweetData['is_retweet'] = tweet['is_retweet']
					except:
						tweetData['is_retweet'] = False

					tweetData['text'] = aTweet
					tweetData['created_at'] = tweet['created_at']

					if len(aTweet) != 0:
						if tweetData['is_retweet']:
							self.validRetweets.append(tweetData)
						else:
							self.validTweets.append(tweetData)


	def createNgrams(self, tweet, N, removeAllStopWords):

		tweetLength = len(tweet)

		if N > tweetLength:
			return None

		cleanedTkns = []
		for token in tweet:
			tkn = self.__checkStopWords(token)
			print(token, tkn)
			if tkn != None:
				cleanedTkns.append(tkn)
		
		if N == 1:
			return cleanedTkns

		else:

			if removeAllStopWords:
				tokens = cleanedTkns
			else:
				tokens = tweet

			ngrams = []

			for i in range(len(tokens) - N+1):
				ngram = tokens[i: i+N]

				print('ngram:', ngram, 'From:', i, 'To:', i + N - 1)

				ngrams.append(ngram)

			if len(ngrams) != 0: 
				return ngrams


	def __removePeriods(self, word):
		fixedWord = ''
		if (word[-1] == '.' and word[-2] in self.letters) or (word[0] == '.'. and word[1] in letters)
			for c in range(len(word)):
				if word[c] != '.':
					fixedWord += word[c]
				else:
					if c != 0 and c != len(word)-2:
						if word[c-1] in self.ints and word[c+1] in self.ints:
								fixedWord += word[c]

		return fixedWord


	def __checkRandomInt(self, word):
		try:
			word = float(word)
			
			if word < 900 or word > 9999:
				return False
			
			else:
				return True
		except:
			return True


	def __checkStopWords(gram):
		if gram in stop_words:
			return None
		else:
			return gram










