import requests
import random

# README - I didn't have time to do a formal one, sorry, but here is info you may need
#
# Visit this link to get the requests library if you don't already have it
# https://requests.readthedocs.io/en/master/user/install/
# Install it, then include it in the project interpreter in PyCharm or similar IDE
#
# I used my bearer token in this project, I hope that is okay. If not, just replace below.

BearerToken = "AAAAAAAAAAAAAAAAAAAAAP8wIAEAAAAAemHrqEB8h2LnQQVC0SeJHxYt%2BXk%3Drm7NmrnaQVkDrnovlMzmB3" \
              "ShGLQJUEEpOHrehhnsP4G3jrhEK9"

ELON_CHOICE = 0
KANYE_CHOICE = 1


# format_text
# This function takes in the raw text in the json file for one tweet
# and returns the text with all links and unnecessary line breaks removed
#
# @text The raw "text" of the tweet in the json File
def format_text(text):
    while text.find('https:/') != -1:
        startIndex = text.index('https:/') + 1
        endIndex = text[startIndex:].find(" ")
        if endIndex == -1:
            endIndex = len(text) - 1
            text = text[:text.find('https:/')]
        else:
            endIndex += startIndex
            text = text[:text.find('https:/')] + text[endIndex + 1:]
    text = text.replace('\n\n', '\n').replace('\t', '\n')
    return text


# is_valid_tweet
# This function checks the tweet json file to see if it is holding any media
# or references other users. The is particular tricky because I noticed media
# can exists in 2 different places in the json, but those places may not
# exist in every tweet json, so you must check if they exist before accessing them
#
# @tweet_json the json file for 1 tweet
def is_valid_tweet(tweet_json):
    if str(tweet_json['entities']).find("\'user_mentions\':") != -1:  # see function header for reasoning
        if len(tweet_json['entities']['user_mentions']) != 0:
            return False  # false if it mentions other users
    if str(tweet_json['entities']).find("\'media\':") != -1:
        if len(tweet_json['entities']['media']) != 0:
            return False  # false if there is media (location 1)
    if str(tweet_json).find("\'quoted_status\':") != -1:
        if str(tweet_json['quoted_status']).find("\'entities\':") != -1:
            if str(tweet_json['quoted_status']['entities']).find("\'media\':") != -1:
                if len(tweet_json['quoted_status']['entities']['media']) != 0:
                    return False  # false if there is media (location 2)
    return True


kanye_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=kanyewest&count=3200'
elon_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=elonmusk&count=3200'

# here we specify we that we don't want an replies or re-tweets. We also saw we want the full text of the tweet
data = {'exclude_replies': True, 'include_rts': False, 'tweet_mode': 'extended'}

# providing the bearer to the http request so we can access the tweets.
headers = {'authorization': 'Bearer ' + BearerToken}
elon_r = requests.get(elon_url, params=data, headers=headers) # get elon tweets
elon_tweets = elon_r.json()
num_elon_tweets = len(elon_tweets)

kanye_r = requests.get(kanye_url, params=data, headers=headers)  # get kanye tweets
kanye_tweets = kanye_r.json()
num_kanye_tweets = len(kanye_tweets)

# variables used for the stats of the user
kanye_index = 0
kanye_correct = 0
kanye_total = 0
elon_index = 0
elon_correct = 0
elon_total = 0
total = 0

# play the game

print("Welcome to the tweet game!")
print("Below, a tweet will be displayed you must enter weather it is authored by Elon Musk or Kanye West")
print("Good Luck!")
print()
print()

done = False
while not done:
    choice = random.randint(0, 1)  # 0 is Elon, 1 is Kanye

    if choice == ELON_CHOICE:  # if we have an elon tweet
        tweet_valid = is_valid_tweet(elon_tweets[elon_index])  # make sure the tweet is valid
        while not tweet_valid:
            elon_index = elon_index + 1
            tweet_valid = is_valid_tweet(elon_tweets[elon_index])
            if tweet_valid:
                if format_text(elon_tweets[elon_index]['full_text']) == "":  # ***Some tweets are just links (weird)
                    tweet_valid = False                                      # so this is necessary***
        print("Tweet:")
        print(format_text(elon_tweets[elon_index]['full_text']))  # print the formatted tweet
        ans_good = False
        while not ans_good:  # evaluate the answer given by the user
            ans = input("Is this tweet written by Elon or Kanye (E or K): ")
            if ans == "E":
                elon_correct = elon_correct + 1
                print("Correct!")
                ans_good = True
            elif ans == "K":
                print("Sorry, but that is wrong")
                ans_good = True
            else:
                print("Please enter either E or K")
        elon_index = elon_index + 1  # we go to the next tweet and increment the total number of Elon tweets
        elon_total = elon_total + 1

    else:  # We have a kanye tweet
        tweet_valid = is_valid_tweet(kanye_tweets[kanye_index])  # make sure the tweet is valid
        while not tweet_valid:
            kanye_index = kanye_index + 1
            tweet_valid = is_valid_tweet(kanye_tweets[kanye_index])
            if tweet_valid:
                if format_text(kanye_tweets[kanye_index]['full_text']) == "":  # ***Some tweets are just links (weird)
                    tweet_valid = False                                        # so this is necessary***
        print("Tweet:")
        print(format_text(kanye_tweets[kanye_index]['full_text']))
        ans_good = False
        while not ans_good:  # evaluate the answer given by the user
            ans = input("Is this tweet written by Elon or Kanye (E or K): ")
            if ans == "K":
                kanye_correct = kanye_correct + 1
                print("Correct!")
                ans_good = True
            elif ans == "E":
                print("Sorry, but that is wrong")
                ans_good = True
            else:
                print("Please enter either E or K")
        kanye_index = kanye_index + 1  # we go to the next tweet and increment the total number of Kanye tweets
        kanye_total = kanye_total + 1

    total = total + 1

    print("Your number of correct Elon Tweets is: " + str(elon_correct) + "/" + str(elon_total))
    print("Your number of correct Kanye Tweets is: " + str(kanye_correct) + "/" + str(kanye_total))
    print("Your total number of correct tweets is: " + str(elon_correct + kanye_correct) + "/" + str(total))
    print()

    valid = False
    while not valid:  # ask if they want to play again
        YorN = input("Would you like to play again(Y/N): ")
        if YorN == "Y":
            valid = True
        elif YorN == "N":
            valid = True
            done = True
        else:
            print("Not Y or N, please enter again")

print("Your number of correct Elon Tweets is: " + str(elon_correct) + "/" + str(elon_total))
print("Your number of correct Kanye Tweets is: " + str(kanye_correct) + "/" + str(kanye_total))
print("Your total number of correct tweets is: " + str(elon_correct + kanye_correct) + "/" + str(total))