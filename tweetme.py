import random, json, sys, os
from time import gmtime, strftime

# This code post the tweet from the json file to tweeter

tweets_to_send = [2,'Super tweet','Superpuper_tweet']
#strategy = [[]]
#actions= [104,115,100]

#optimal_strategy = \
#[[115,115,115,115,115,115,115,115,115,115],\

#gen_size = max(int(sys.argv[1]),10) # ------------>  qty of species in one generation
#with open("./tweets.json", "w") as f:
#    json.dump(tweets_to_send,f)
with open("./tweets.json") as f:
    tweets_to_send = json.load(f)
#for i in range(gen_size):
#  strategy = [[random.choice(actions) for j in range(10)] for i in range(26)]
#  with open("./species/specie"+str(i)+".json", "w") as f:
#    json.dump(strategy,f)
    f.closed
#cmd_line="echo -e \'t New line in tweet\\nq\\n\' | rainbowstream"
#cmd_line="echo -e \'\\n\\nt Quick brown fox "+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"\\nq\\n\' | rainbowstream"
cmd_line="echo -e \'\\n\\nt "+tweets_to_send[tweets_to_send[0]]+" "+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"\\nq\\n\' | rainbowstream"
print (cmd_line)
returned_value = os.system(cmd_line)
print('returned value:', returned_value)
print(tweets_to_send[0])
if tweets_to_send[0] == len(tweets_to_send)-1:
	tweets_to_send[0] = 0
tweets_to_send[0]=tweets_to_send[0]+1
with open("./tweets.json", "w") as f:
    json.dump(tweets_to_send,f)
    f.closed