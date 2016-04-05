import re
import json
import networkx as nx
import itertools
from datetime import datetime,timedelta
import TweetGraph
import TruncateNum




# Define variables
tmax=''
tnew=''
tmin=''
output_result=[]

# Input and output file path
tweets_filename = '.\\tweet_input\\tweets.txt'
output_filename = '.\\tweet_output\\output.txt'


# Data clean: open input file and remove rate_limit rows
try:
    tweets_file = open(tweets_filename, "r+")
    d = tweets_file.readlines()
    tweets_file.seek(0)
    # Remove rate-limit message from input file
    for i in d:
        if '''{"limit":{"track":''' not in i:
            tweets_file.write(i)
    tweets_file.truncate()
    tweets_file.close()
# Throw an error if the input file can not be opened. And then exit.
except IOError:
    print('File cannot be opened:',tweets_filename)
    exit()

# Create a graph object G
G = nx.Graph()

# Calculate average_degree of a vertex in a Twitter hashtag graph over a 60-second sliding window
if __name__ == '__main__':
    try:
        tweets_file = open(tweets_filename, "r+")
        try:
            # Loop through input file

            for line in tweets_file:
                   # Read in one line of the file, convert it into a json object
                   tweet = json.loads(line.strip())
                   # Only messages contain 'text' field is a tweet
                   if 'text' in tweet:
                       #Get created_at and hashtag information from input file
                        created_at = tweet['created_at']
                        hashtags = []
                        for hashtag in tweet['entities']['hashtags']:
                            hashtags.append(hashtag['text'])

                    # First line message handling
                        # Assign values to time variables to initiate 60-second sliding window
                        if tmax =='':
                            tnew = datetime.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y')
                            tmax = datetime.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y')
                            tmin = tmax-timedelta(minutes = 1)
                        # Check if there is any 'text' information in hashtag field
                            # If hashtag is empty output result = 0.00
                            if len(hashtags)== 0:
                                output_result = '0.00 \n'
                                with open(output_filename, 'a') as f:
                                    f.writelines(output_result)
                                f.close()
                            # Otherwise add note(s) and edge(s) into graph object G and then calculate average_degree
                            else:
                                tweetgraph = TweetGraph.GetAveDegree(hashtags,created_at)
                                AveDegree = tweetgraph.TweetAveDegree()
                                trunum= TruncateNum.CTruncateNum(AveDegree)
                                output_result = trunum.ChopNum()
                                with open(output_filename, 'a') as f:
                                    f.writelines(output_result)
                                f.close()
                    # Message handling except for the first line
                        # If created_at is earlier than 60 seconds window, this line will be discarded. The new output value equals to the previous output value
                        elif tnew < tmin:
                                with open(output_filename, 'a') as f:
                                    f.writelines(output_result)
                                f.close()
                        # If created_at is inside the 60 seconds window
                        elif tmin <= tnew <= tmax:
                          # Check if there is any 'text' information in hashtag field
                            # If the hashtag is empty, the new output value is equal to previous output value
                            if len(hashtags)== 0:
                                with open(output_filename, 'a') as f:
                                    f.writelines(output_result)
                                f.close()
                            # Otherwise add note(s) and edge(s) into graph object G, calculate G's average_degree
                            else:
                                tweetgraph = TweetGraph.GetAveDegree(hashtags,created_at)
                                AveDegree = tweetgraph.TweetAveDegree()
                                trunum= TruncateNum.CTruncateNum(AveDegree)
                                output_result = trunum.ChopNum()
                                with open(output_filename, 'a') as f:
                                    f.writelines(output_result)
                                f.close()
                        # If created_at time is later than 60 seconds' window. Update the 60-second window
                        else:
                            tmax = tnew
                            tmin = tmax-timedelta(minutes = 1)
                            # Check if there are any old edges in graph
                            old_edge = list((u,v) for u,v,d in G.edges_iter(data = True) if d['time'] < tmin)
                            # Remove old edges if they are existed
                            if len(old_edge) > 0:
                                G.remove_edges_from(old_edge)
                             # Calculate average_degree based on new graph
                                # If empty 'text' in hashtags field, calculate average_degree based on the modified graph
                                if len(hashtags) == 0:
                                    degrees = G.degree()
                                    sum_of_edges = sum(degrees.values())
                                    average_degree = sum_of_edges/G.number_of_nodes()
                                    trunum = TruncateNum.CTruncateNum(average_degree)
                                    output_result = trunum.ChopNum()
                                    with open(output_filename, 'a') as f:
                                        f.writelines(output_result)
                                    f.close()
                                # Else add new nodes and edges to the graph and calculate average_degree
                                else:
                                    tweetgraph = TweetGraph.GetAveDegree(hashtags,created_at)
                                    AveDegree = tweetgraph.TweetAveDegree()
                                    trunum = TruncateNum.CTruncateNum(AveDegree)
                                    output_result = trunum.ChopNum()
                                    with open(output_filename, 'a') as f:
                                            f.writelines(output_result)
                                    f.close()
                            # If there is no old edge
                                # If hashtag is empty, new output value equals to the previous output value
                            else:
                                if len(hashtags) == 0:
                                    with open(output_filename, 'a') as f:
                                        f.writelines(output_result)
                                    f.close()
                                # Else add new node(s) and edge(s) to the graph and then calculate average_degree
                                else:
                                    tweetgraph = TweetGraph.GetAveDegree(hashtags,created_at)
                                    AveDegree = tweetgraph.TweetAveDegree()
                                    trunum= TruncateNum.CTruncateNum(AveDegree)
                                    output_result = trunum.ChopNum()
                                    with open(output_filename, 'a') as f:
                                            f.writelines(output_result)
                                    f.close()
        # Close input file
        finally:
                tweets_file.close()
    except IOError:
        pass

