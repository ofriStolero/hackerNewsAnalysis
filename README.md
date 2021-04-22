# hackerNewsAnalysis
A simple program which analysis comments to top stories from HN
given a phrase the program will scan top stories with that phrase in the title.
then sentiment analysis is used to determine the sentiment of each comment.
the response includes the average and median of each sentiment (positive,negative,mixed,neutral).

How to run-
Simply run the handler_git.py file.
make sure to add the relevant AWS credentials in credentials.txt.

How it works-
As the HN API is very slow, we used cached memory in the form of two txt files - comments.txt, stories.txt.
this way we can prevent unnecessary API requests and shorten the run time.

Modules and technologies used -
the following modules were used to perform this code -
json
requests
boto3 - AWS sdk
statistics
pprint

as mentioned, the program uses HN API and AWS Comprehend.

