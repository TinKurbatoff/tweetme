# This code will send twits from tweets.json file adding images if needed.
# Usage:
#   ~> python3 tweetme.py [account name]
# where:
#   account name — name of twitter account, this name will be used to load/save OAuth keys
#
# This code to post tweets needs three files:
# 1. 'tweetme_consumer.json' — keeps consumer keys that should be obtained by regitering application at developer.twitter.com
#    if it doesn't exists, it creates this file with predefined keys at Row 17 
# 2. 'OAuth_data.tweetme' — keeps authentification information, it is created automaticaly  after sucsessful authentification
# 3. 'tweets.json' — file with tweets, the first variable is pointer to the tweet to send  
#=========================================================================================
import tweepy,random, json,  os
from sys import argv
from os.path import isfile
from time import gmtime, strftime
import webbrowser

#===================================================
# Consumer (developers) keys, will be used for OAuth
#===================================================
try:
    # Oens file with consumer keys thas was got from twitter dev account 
    f = open("tweetme_consumer.json", 'r')
    consumer_keys = json.load(f)
    f.close()
except IOError:
    # If no such file we create it with 'dumb' data, update it it with your's keys
    consumer_keys = { 'consumer_key' : 'Insert_your_consumer_key',  'consumer_secret' : 'Insert_your_consumer_private_key'}
    f = open("tweetme_consumer.json", 'w')
    io_result = json.dump(consumer_keys,f)
    f.close()
    # message for debug purpose 
    # print('Saving consumer keys. I/O problems:',io_result)    


consumer_key = consumer_keys['consumer_key']  #'Public developer key'
consumer_secret = consumer_keys['consumer_secret'] # 'Private developer key'

#==============================================
# Loading tweeets' texts from file
#==============================================
try:
    with open("./tweets.json") as f:
        tweets_to_send = json.load(f)
        f.closed
except IOError: 
    # if no such file - create a sample tweets db, first number is twit index [1...]
    tweets_to_send = [1,'Hello world','My second twit!']

# Random selecton of twits
#for i in range(gen_size):
#  strategy = [[random.choice(actions) for j in range(10)] for i in range(26)]


# Select the current message that will be twitted today
message=tweets_to_send[tweets_to_send[0]] #+" "+strftime("%Y-%m-%d %H:%M:%S", gmtime())
print ('Twit msg:\'%s\'' % message)

#========================================
#  Initialazing remote connection to API
#========================================
# OAuth process, firstly authentificating this application:
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Retreiving OAuth keys file name from the command string 
try: 
    OAuth_data_file_name = argv[1]
    OAuth_data_file_name += '.oauth' # File name extention '*.oauth'
except IndexError:
    OAuth_data_file_name = "OAuth_data.tweetme" # default access keys(tokens) file for personal use

# Load Oath tokens from file with predefined name from the command string
try:
    f = open(OAuth_data_file_name, 'r')
    saved_acc_tokens = json.load(f)
    f.closed
    access_token = saved_acc_tokens['access_token']
    access_token_secret = saved_acc_tokens['access_token_secret'] 
except IOError: # No file exists or no access
    access_token = '' # So, no saved access keys for today
    
#========================================================================
# If there are no tokens saved — create a new pair / or use existing ones 
#========================================================================
if access_token == '' :
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
    print (redirect_url)
    webbrowser.open(redirect_url)
    #print(webbrowser.get('Verifier'))

# === Get these tokens  from growser response link in manual mode - will make it later in automatic mode
    verifier = input('Verifier (from browser link):')
    token = input('Token (from browser link):')
#   token = webbrowser.session.get('request_token')
#    webbrowser.session.delete('request_token')
    #
    # Send tokens to get response from twitter API with permanent account OAuth keys
    #
    auth.request_token = { 'oauth_token' : token,'oauth_token_secret' : verifier }
    try:
        response = auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')    
    print("API auth response:", response)
    # Finally, save these OAuth keys into file
    OAuth_keys = { 'access_token' : response[0],  'access_token_secret' : response[1] }
    f = open(OAuth_data_file_name, 'w')
    io_result = json.dump(OAuth_keys,f)
    f.close()
    # message for debug purpose 
    print('Saving OAuth keys. I/O problems:',io_result)    
    #print (auth.request_token)  # debugging 

else: # Or just quickly login to authentificated account
    auth.set_access_token(access_token, access_token_secret)

#=========================================
# Initializing API for tweeting
#=========================================    
# Creation of the API connection interface, using authentication
api = tweepy.API(auth)

# Creates the user object (connecting to twitter account). 
# The me() method returns the user whose authentication keys were used.
user = api.me()

# Displays information about choosen twitter profile
#
#print('Full user info (unformatted):', user) # debugging 
print('Name: ' + user.name)
#print('Location: ' + user.location)
print('Friends: ' + str(user.friends_count))

#===========================
# Preparing image to publish
#===========================
#cmd_string = 'echo ls'
#os_result = os.system(cmd_string)
#print (os_result) #debugging

#
# Set image path
#
imagePath = '/home/root/images/image.jpg'

#=========================
# Finally, send the tweet.
#=========================

# Checking if image file exists 
if not isfile(imagePath): 
    # I.  Sample method, used to update a status
    print("Image file \''%s\'' is not found!" % imagePath )
    api.update_status(message) 
else:
    # II. Anther method, used to update a status with an image
    api.update_with_media(imagePath, message) 

# 
# As a result — moving pointer to the next tweet in the base and saves updated information to the file.
print("Current twit index: %s." % tweets_to_send[0]) # Current number in the queue
if tweets_to_send[0] == len(tweets_to_send)-1:
	tweets_to_send[0] = 0
tweets_to_send[0] += 1
with open("./tweets.json", "w") as f:
    json.dump(tweets_to_send,f)
    f.closed
