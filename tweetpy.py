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
# 3. 'tweets.json' — file with tweets, the first variable is pointer to the tweet to send. This file is used  
#    when <accont name>.json file is absent.
#=========================================================================================
import tweepy,random, json,  os, re
from sys import argv
import os
from os.path import isfile
from time import gmtime, strftime
import webbrowser

#===================================================
# Consumer (developers) keys, will be used for OAuth
#===================================================
def init_dev_account(devkeys_file_name='tweetpy_dev_keys.json'): # devkeys_file_name — file with develper keys
    try:
        # Opens file with consumer keys thas was got from twitter dev account 
        f = open(devkeys_file_name, 'r')
        consumer_keys = json.load(f)
        f.close()
    except IOError: 
        # If no such file we create it with 'dumb' data, update it it with your's keys
        consumer_keys = { 'consumer_key' : 'Insert_your_consumer_key',  'consumer_secret' : 'Insert_your_consumer_private_key'}
        f = open(devkeys_file_name, 'w')
        io_result = json.dump(consumer_keys, f)
        f.close()
        # message for debug purpose 
        # print('Saving consumer keys. I/O problems:',io_result)
    return consumer_keys # An array ['consumer_key': public key,  'consumer_secret': private key]    


#==============================================
# Loading tweeets' texts from file
#==============================================
def load_tweets_from_file(tweets_file_name='tweets.json'): 
    try: 
        tweets_file_name = argv[1]
        tweets_file_name += '.json' # File name extention for twits '[ACCOUNT NAME].json'
        try: # check if file exists
          isfile(tweets_file_name)
        except IOError: # account defined, but file not exists
            print ("File %s not found, will be created with dafault tweets." % tweets_file_name)
    except IndexError:
        print("no data in command line")
        print("Uses default filr name ", tweets_file_name)
    # There is not account specified, use standard tweets file name
    #    tweets_file_name  = "./tweets.json" # default  file  name for tweets text


    # try to load default tweets
    try:
        with open(tweets_file_name) as f:
            tweets_to_send = json.load(f)
            f.closed
    except IOError: 
        # if no such file - create a sample tweets db, first number is twit index [1...]
        print ("...Tweets texts files were not found. Use default tweets.")
        tweets_to_send = [1,'Hello world','./image1.jpg','My second twit!','./image2.jpg']

    # Random selecton of twits
    #for i in range(gen_size):
    #  strategy = [[random.choice(actions) for j in range(10)] for i in range(26)]
    # Select the current message and picture that will be twitted today
    # The first number in json — number of tweet to post
    # Json format: 
    #   1. the very first number — number of a record with twit to send
    #   2. the index record — twit text
    #   3. tht index+1 — a path to the picture to add to twitt
    message=tweets_to_send[tweets_to_send[0]] #+" "+strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print ( 'Twit msg:\'%s\'' % message+strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
    image_path=tweets_to_send[tweets_to_send[0]+1]
    # 
    # As a result — moving pointer to the next tweet in the base and saves updated information to the file.
    print("Current twit index: %s." % tweets_to_send[0]) # Current number in the queue
    if tweets_to_send[0] == len(tweets_to_send)-2: # if that is a last tweet — we start over from the beggining
        tweets_to_send[0] = 1
    else:
        tweets_to_send[0] += 2
    with open(tweets_file_name, "w") as f:
        json.dump(tweets_to_send,f)
        f.closed    

    return message, image_path

#========================================
#  Initialazing remote connection to twitter API
#========================================
# OAuth process, firstly authentificating this application:
def connect_to_twitter(consumer_key, consumer_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    return auth
    # Retreiving OAuth keys file name from the command string 
    #try: 
    #    OAuth_data_file_name = argv[1]
    #    OAuth_data_file_name += '.oauth' # File name extention '*.oauth'
    #except IndexError:
    #    print("Uses the default file for connect to user twitter account: ",OAuth_data_file_name) # default access keys(tokens) file for personal use

#========================================
#  Read keys from file to initilize user account
#========================================
# OAuth process, firstly authentificating this application:
def read_user_tokens_from_file(OAuth_data_file_name = 'OAuth_data_tweetpy.oauth'):
    # Load Oath tokens from file with predefined name from the command string
    try:
        f = open(OAuth_data_file_name, 'r')
        saved_acc_tokens = json.load(f)
        f.closed
        access_token = saved_acc_tokens['access_token']
        access_token_secret = saved_acc_tokens['access_token_secret'] 
    except IOError: # No file exists or no access
        access_token = '' # So, no saved access keys for today
        access_token_secret = ''
    return access_token, access_token_secret    # access_token — points to account , access_token_secret — account security token
    
#========================================================================
# If there are no tokens saved — create a new pair / or use existing ones 
#========================================================================
def create_new_account_tokens(OAuth_data_file_name='OAuth_data_tweetpy.oauth', verifier='', token=''):
    # It works in the following way:
    #    ask twitter for couple keys by logging to account online by a special link
    #    having these keys (simple numbers) send them to API 
    #    in result we have 
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('░▒▓█ Error! Failed to get request token.')
        print (redirect_url)
    webbrowser.open(redirect_url)
        #print(webbrowser.get('Verifier'))

    # === Get these tokens  from growser response link in manual mode - will make it later in automatic mode
    token = input('Token (from browser link):')
    verifier = input('Verifier (from browser link):')
        #   token = webbrowser.session.get('request_token')
        #    webbrowser.session.delete('request_token')
        #
        
    # Send tokens to get response from twitter API with permanent account OAuth keys
    #
    auth.request_token = { 'oauth_token' : token,'oauth_token_secret' : verifier }
    
    try:
        response = auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('░▒▓█ Error! Failed to get access token.')    
    print("API auth response:", response)
    # Finally, save these OAuth keys into file
    OAuth_keys = { 'access_token' : response[0],  'access_token_secret' : response[1] }
    f = open(OAuth_data_file_name, 'w')
    io_result = json.dump(OAuth_keys,f)
    f.close()
    # message for debug purpose 
    print('Saving OAuth keys. I/O problems:',io_result)    
    #print (auth.request_token)  # debugging 
    return OAuth_keys['access_token'], OAuth_keys['access_token_secret'] 

#========================================================================
# Login to the account with two keys ("tokens")
#========================================================================
def login_to_account(access_token, access_token_secret):
    # Login to authentificated account
    result = auth.set_access_token(access_token, access_token_secret)
    return result  
        

#
# Send tweet if everythng is set up
#
#imagePath = '/home/root/images/image.jpg'
#=========================
# Finally, send the tweet.
#=========================
def send_tweet_now(account_api, message, image_path):
    print('Sending twitt...')
    # Checking if image file exists 
    if not isfile(image_path): 
    # I.  Sample method, used to update a status without image
        print("░▒▓█ Image file %s is not found!" % image_path )
        try: 
            result = account_api.update_status(message) 
        except tweepy.error.TweepError: 
            print ('Duplicated tweet. We recommend to reconsider text used.')
            result = 'fail.'
            #result  = tweepy.error.TweepError.response.text
    else:
    # II. Anther method, used to update a status with an image
        result = account_api.update_with_media(image_path, message) 
    return result    



#=========================================
# ***** MAIN FUNCTION
#=========================================    

if __name__ == "__main__":
    image_file_name = ''
    twitter_account_name = ''
    text_of_the_tweet = ''
    if ('-l' in argv): 
        try: 
            twitter_account_name = argv[argv.index('-l') + 1]
        except: 
            print('use: tweetpy -l <account name>') 
            twitter_account_name = ''
    
    if ('-i' in argv): 
        try: 
            image_file_name = argv[argv.index('-i') + 1]
        except: 
            print('use: tweetpy -i <image file>') 
    
    if ('-t' in argv): 
        try: 
            text_of_the_tweet = argv[argv.index('-t') + 1] 
        except: 
            print('use: tweetpy -t \"<tweet text>\"') 
            text_of_the_tweet = 'Test. '+strftime("%Y-%m-%d %H:%M:%S", gmtime())
    # --- results of arguments parsing
    print('############# TWITTER SENDER APP #####################')
    print('-----------------------------—————————————————————————')
    print("Parsed arguments:")
    print("Account: \'", twitter_account_name,'\'')
    print("Image: \'", image_file_name,'\'')
    print("Text: \'", text_of_the_tweet,'\'')
    print('-----------------------------—————————————————————————')
    # ===================================
    ##### CONNECTING TO TWITTER
    # ===================================                        
    dev_keys = init_dev_account('tweetme_consumer.json')
    auth = connect_to_twitter(dev_keys['consumer_key'],dev_keys['consumer_secret'])
    # Creates the user object (connecting to twitter account). 
    # The me() method returns the user whose authentication keys were used.
    access_token, access_token_secret = read_user_tokens_from_file(twitter_account_name+'.oauth')
    if (access_token==''):
          access_token, access_token_secret=create_new_account_tokens(twitter_account_name+'.oauth')
    login_to_account(access_token, access_token_secret)

    # Displays information about choosen twitter profile
    #
    # Creation of the API connection interface, using authentication
    twitter_api = tweepy.API(auth)    
    user = twitter_api.me() # load user data for
    #print('Full user info (unformatted):', user) # debugging 
    print('Name: ' + user.name)
    #print('Location: ' + user.location)
    print('Friends: ' + str(user.friends_count))



    #===========================
    # Preparing image to publish
    #===========================
    #os.system('python3 dnldgoogle.py \''+image_path+'\' -d 1 ')
    #print('Converting image file resolution...')
    #os.system('convert \''+image_path+'\' -resize 4096  \''+image_path+'\' ')
    #cmd_string = 'echo ls'
    #os_result = os.system(cmd_string)
    #print (os_result) #debugging
    
    result = send_tweet_now(twitter_api,text_of_the_tweet, image_file_name)
    print("Result of tweet: ", result)
