import json
import requests
import boto3
import statistics
import pprint

def getMean(num): return round(statistics.mean(num),2)	
def getMedian(num): return round(statistics.median(num),2)
			

phrase = input("enter phrase: (to exit enter 0): ")

credentials = json.load(open("credentials.txt"))

client = boto3.client('comprehend',aws_access_key_id = credentials['aws_access_key_id'],aws_secret_access_key = credentials['aws_secret_access_key'],region_name='us-west-2')
stories = json.load(open("stories.txt"))
comments = json.load(open("comments.txt"))

while phrase != "0":
	# get the top 500 stories from HN
	r = requests.get(url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty")
	ids = r.json()

	positive = []
	negative = []
	mixed = []
	neutral = []
	
	for id in ids :
		id = str(id)
		
		# if we have the story save, load it otherwise get it from HN
		if id in stories:
			story = stories[id]
			
		else:
			r = requests.get(url = "https://hacker-news.firebaseio.com//v0/item/"+str(id)+".json?print=pretty")
			story = r.json()
			title = story["title"] if "title" in story  else ""
			kids = story["kids"] if "kids" in story else []
			stories[id] = {"title" : title , "kids" : kids}
			
		if phrase in story["title"]:
			
			#go over all the comments ('kids')
			for comment_id in story["kids"]:
				comment_id = str(comment_id)
				
				#if we have the comment saved, load it (with sentiment), else get information from HN and AWS comprehend
				if comment_id in comments :
					comment = comments[comment_id]
				else:
					r = requests.get(url = "https://hacker-news.firebaseio.com//v0/item/"+str(comment_id)+".json?print=pretty")
					comment = r.json()
					if "text" not in comment:
						continue
					
					if len(comment['text']) > 5000 : 
						text = comment['text'][:5000] 
					else: 
						text = comment['text']
					
					response = client.detect_sentiment(Text=text,LanguageCode='en')
					if response['ResponseMetadata']['HTTPStatusCode'] != 200 :
						break
						
					comments[comment_id] = {"text" : comment["text"] , "SentimentScore" : response['SentimentScore']}
					comment = comments[comment_id]
						
				positive.append(comment['SentimentScore']['Positive'])
				negative.append(comment['SentimentScore']['Negative'])
				mixed.append(comment['SentimentScore']['Mixed'])
				neutral.append(comment['SentimentScore']['Neutral'])
	
	#if no stories were loaded return error
	if len(positive) == 0 :
		response = {
		"statusCode": 416,
		}
		
	else :
		ans = {"comments" : len(positive)}
		ans["positive"] = {"avg" : getMean(positive), "median" : getMedian(positive)}
		ans["neutral"] = {"avg" : getMean(neutral), "median" : getMedian(neutral)}
		ans["negative"] = {"avg" : getMean(negative), "median" : getMedian(negative)}
		ans["mixed"] = {"avg" : getMean(mixed), "median" : getMedian(mixed)}
		
		response = {
		"statusCode": 200,
		"body": json.dumps(ans)
		}
		
	pprint.pprint(response)	
	json.dump(stories, open("stories.txt",'w'))
	json.dump(comments, open("comments.txt",'w'))
	phrase = input("enter phrase: (to exit enter 0): ")	

