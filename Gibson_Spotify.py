# Name: Clay Gibson
# Date: 30 January 2015
# Description: Python Coding Assignment for Spotify
# File Path: ~/Dropbox/Senior Year/Term 2/Gibson_Spotify.py

import sys, argparse
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
import time
import spotipy

cached_data = {}			# Storage for search results
sp = spotipy.Spotify()		# Used for accessing Spotify API
	
# Preprocess takes in a string and returns a list of sentences broken down 
# into word tokens using nltk

def preprocess(text_input):
	sentence_tokens = [] 	# Storage for list of tokens organized by sentence
	
	# Define a tokenizer that won't break up contractions
	tokenizer = RegexpTokenizer("[\w']+") 	
	# For every sentence in text input, add list of tokens to sentence_tokens	
	for x in sent_tokenize(text_input): 		
		sentence_tokens.append(tokenizer.tokenize(x))
	return sentence_tokens


# Force takes in tokenized sentence and then finds song titles within 
# using the following method: search full sentence. If no search result 
# match, search sentence without last word. continue until you find a 
# match or get down to a single word. once match found, do process on 
# rest of unmatched words. 

def force(token_input, stm, tic, dur):
	length = len(token_input)
	x = 0						# Start token
	y = length					# End token
	
	while (y >= x):
		# if search has taken more time than specified in dur, break
		if dur is not None and (time.time() - tic > dur): 
			print "\nUnable to retrieve full results in specified time"
			break
		# Combine tokens in range x to y into a string
		frag = ' '.join(token_input[x:y]) 
		# Deal with case in dictionary; see line 70
		frag = frag.lower()
		# First check cached data
		if frag in cached_data: 
			# Result stored as list of Song Title, Artist, Spotify Link
			res = (frag, cached_data[frag][0], cached_data[frag][1])
		# If not in cached data, search with the API call
		else:
			# Result stored as list of Song Title, Artist, Spotify Link
			res = search_for_title(frag)
			
		# If result is found
		if res != 0:
			print_res(res)		
			# Move onto rest of input
			x = y
			y = length
		
		# If no result found and only one word left
		elif (y-x == 1):
			# If stemmer option chosen, search song titles with the
			# stem of the word (ex. eyes -> eye; running -> run)
			if stm == 1: 
				stemmer = SnowballStemmer("english")
				res = search_for_title(stemmer.stem(frag))
				if res != 0:
					print_res(res)
			# Move onto rest of input
			x = y
			y = length
		
		else: 
			# Repeat process looking for phrase minus last word
			y -= 1		


# Search for a track in Spotify API, cache search results
# return 0 if not found, list if found.

def search_for_title(my_string):
	# Search for string in titles only
	results = sp.search(q = 'track:'+ my_string, type='track', limit=40)
	items = results['tracks']['items']
	for i, t in enumerate(items):
		# For each item of the search results, add to dictionary a tuple of 
		# artist and Spotify url with the song name as key
		cached_data[t['name'].lower()] = (t['artists'][0]['name'], 					
										  t['external_urls']['spotify'])
		# If the name of the song matches the search, return a list of the
		# song title, artist name, and Spotify url
		if t['name'].lower() == my_string:
			return (t['name'], 
					t['artists'][0]['name'], 
					t['external_urls']['spotify'])
	return 0


# Take in a list of tokenized sentences and max length. Returns a list of the
# sentences broken down with a max length of n 

def generate_short_sentences(token_sentences, n):
	token_output= []					# Storage for results to return
	# For each tokenized sentences in the input...
	for x in token_sentences:
		# if the sentence is longer than the specified max length (n)
		# break the sentence into segments of length n and store them
		# in token_output
		if len(x) > n:
			i = 0
			while i + n <= len(x):
				token_output.append(x[i:i+n])
				i = i+n
			token_output.append(x[i:len(x)])
		# if sentence is not longer than max length, add it to token_output	
		else:
			token_output.append(x)
	return token_output
				
				
# Given list of Song Title, Artist, Spotify Link, print returned song results
# in formatted way: Title - Artist - Link

def print_res(res):
	# Print Title - Artist - Link (song title is capitalized)
	print (' - '.join((res[0].title(),res[1],res[2])))
	
	
def main(argv): 
	# Take in arguments and options from the command line
	# Usage: 
	# Gibson_Spotify_V2.py [-h] [-d DIVIDE] [-s {0,1}] [-t TIME] message                                    
	parser = argparse.ArgumentParser()
	parser.add_argument("message", type=str,
       			 	help = "message to translate into Spotify song titles")
	parser.add_argument("-d", "--divide", type = int,
					help = "divide long sentences into subsentences of length "
							"DIVIDE to improve return time")
	parser.add_argument("-s", "--stemmer", type = int, choices = [0,1],
					help = "search for stem if word cannot be found")
	parser.add_argument("-t", "--time", type = int, 
					help = "return the best results in TIME number of seconds")
	args = parser.parse_args()
	
	my_message = args.message
	print "\nSearching for Song Title Poem for:\n\"" + my_message + "\"\n...\n"
	
	# Break down string message into list of tokenized sentenced
	my_sentences = preprocess(my_message)
	# If option divide is turned on, create list of tokenized sentences
	# with max length args.divide
	if args.divide > 0:	
		my_sentences = generate_short_sentences(my_sentences,args.divide)
	
	# Take in the max time to return and check the current time
	duration = args.time
	start_time = time.time()
	
	# For each tokenized sentence (or broken down sentence), run search 
	# procedure as specified in force function
	for x in my_sentences:
		if len(x) > 0:
				force(x, args.stemmer, start_time, duration)
		 

if __name__ == "__main__":
    	main(sys.argv)