# Creating Poetry with Spotify’s Public API

Usage: Gibson_Spotify.py [-h] [-d DIVIDE] [-s {0,1}] [-t TIME] message
Arguments:
	message					message to translate into Spotify song titles
Options:
	-h 						shows this help message and exit
	-d DIVIDE				divide long sentences into subsentences of length
                        	DIVIDE to improve return time
	-s {0,1}				search for stem if word cannot be found
	-t TIME					return the best results in TIME number of seconds
	
Examples:
Gibson_Spotify.py -h
	
Gibson_Spotify.py "if i can't let it go out of my mind"
	
Gibson_Spotify.py -t 10 "if i can't let it go out of my mind"
	
Gibson_Spotify.py -s 1  -t 60 "if i can't let it go out of my mind i'm scared. my 	stupid heart my stupid mind will try finding a way home home to you letting you know all the ways i want the world to stop with you" 
	
Gibson_Spotify.py -s 1  -t 60 -d 10 "if i can't let it go out of my mind i'm scared. my 	stupid heart my stupid mind will try finding a way home home to you letting you know all the ways i want the world to stop with you" 
	

# Method for finding songs 

In general, given a string input of "if i can't let it go out of my mind", this program searches for titles in the following order (capitalization does not matter):

"if i can't let it go out of my mind"
"if i can't let it go out of my"
"if i can't let it go out of"	
...
"if i can't"

If there is a match, we print the details (song title, artist, url) and move onto the rest of the input:

"let it go out of my mind"
"let it go out of my"
"let it go out of"
...
"let it go"

And so on until there are no more words in the sentence. 


# Run-time and Searches

How many searches will it take? 
Given a string of length n, you will make n(n+1)/2 searches in the worst case scenario. That means that the time to find results will increase as a function of n^2. If you predict that will take too long, use the option to specify a time limit (using the -t option). Once that amount of time has elapsed, the program will stop. 

Can time be improved?
1) In order to speed up the search process, the results from API searches are stored in a dictionary (cached_data). Before searching for a title with the API, we check dictionary with the song title as the key. 

2) The -d option allows you to split sentences that are too long into smaller subsections. Thus if you had a sentence with 1000 words, you would make 500,500 searches in the worst case. Using -d 10, you would be making (100)[(10)(11)/2] =  5500 searches. However, the -d option could be splitting up sentences mid song title, meaning that using the -d option might result is less optimal results. 


# Optimality of results

Is this method optimal? 
The results of this method are often good. However, this method will not always give you the optimal results. Finding the longest song title might break up later song title possibilities. For example, if you're given the string: "coming home is where the heart is" this method would give you:
	Coming Home
	Is
	Where the heart is

However, a more optimal solution would be: 
	Coming
	Home is Where the Heart is


# Unmatched words


The -s option searches for the stem of an individual word. Thus, if you cannot find a song "Eyes," the program will return a song "Eye." If "running" is not found, it will search "run." This helps cut down on the number of unmatched words. 

# Alternative Strategies and Ways to Improve

A. Syntax Trees

Searching the API takes time, so one consideration is to try to reduce the number of searches you perform. If that is the goal, it would help if you could predict which phrases, or groups of words, are likely to be song titles. One way to do this is to create syntax trees for the sentence input you take in. 

For example, "the dog saw a man" would be broken down into:
(S (NP the dog) (VP (V saw) (NP a man)))
Your program would search the root node -- the full sentence. If not found, it would search the children -- NP "the dog" and VP "saw a man", and so on. On one hand, this method would reduce the number of searches. On the other, the accuracy depends on the grammar structure that you implement. You might miss out on "the dog saw" using the above method. 

B. Parallel API Requests

To both increase speed and optimality, you could break the sentence into all possible song title parts. For example, "Clay was here" becomes
	Clay was here
	Clay was
	Clay
	was here
	was
	here
	
You would take this list and run all of the API requests at once. That way you only have to wait on one request (but it might put undue stress on API server). You would then discard the searches without results and piece together the matched parts into a list. There could be many ways to piece these together to form the sentence. You could do all combinations and return the one with fewest elements. 




