#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
import praw
import argparse
import redis
import json
import logging
import traceback


class ArgumentParserError(Exception):
    def __init__(self, message):
        self.message = message


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


logging.basicConfig(filename='bot.log',level=logging.DEBUG)

with open('keys', 'r') as f:
    keys = json.load(f)

logging.info("New session started!")

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

app = Flask(__name__)
bot = Bot(keys['ACCESS_TOKEN'])

sortings = ['controversial', 'hot', 'top', 'new', 'gilded', 'random_rising', 'rising']
numbers = list(range(1, 11))


@app.route("/", methods=['GET', 'POST'])
def receive_message():
    logging.info("receive_message: New {} request".format(request.method))
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       logging.info("receive_message: {}".format(json.dumps(output)))
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    text = message['message'].get('text')
                    logging.info("receive_message: " + text)
                    response_sent_text = proceed(recipient_id, text)
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    logging.error("receive_message: Non-text!!!")
                    response_sent_nontext = make_negative_response()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == keys['VERIFY_TOKEN']:
        logging.info("verify_fb_token: Token verified")
        return request.args.get("hub.challenge")
    logging.info("verify_fb_token: Token not verified")
    return 'Invalid verification token'


def is_image(url):
    return url.endswith(".jpg") or url.endswith(".png")


def send_message(recipient_id, response_text):
    #sends user the text message provided via input response parameter
    success = True
    for message in response_text:
        try:
            if is_image(message):
                bot.send_image_url(recipient_id, message)
            else:
                bot.send_text_message(recipient_id, message)
        except Exception as e:
            success = False
            logging.error("send_message: " + traceback.format_exc())
    return success


def parse(command):
    logging.info("parse: Parse command: {}".format(command))
    parser = ThrowingArgumentParser()
    parser.add_argument('action', default='show_memes', 
        choices=['show_memes', 'show_subscriptions', 'subscribe', 'unsubscribe'], help='What do you want to do?')
    parser.add_argument('--number', '-n', default=1, type=int, choices=numbers, help='Number of memes to display')
    parser.add_argument('--sort', '-s', default='hot', choices=sortings, help='Sorting of memes')
    parser.add_argument('--channels', '-c', default=['all'], nargs='*', help='Channels where to search memes')
    args = parser.parse_args(command)
    args.number = int(args.number)
    assert isinstance(args.number, int)
    assert args.number > 0
    return args


def proceed(recipient_id, text):
    command = text.split()

    if '--help' in command or '-h' in command:
        logging.info("proceed: Help command")
        return [
"""usage: [-h] [--number {""" + ','.join([str(x) for x in numbers]) + """}]
                 [--sort {""" + ','.join([str(x) for x in sortings]) + """}]
                 [--channels [CHANNELS [CHANNELS ...]]]
                 {show_memes,show_subscriptions,subscribe,unsubscribe}
"""     ], []

    try:
        args = parse(command)
        assert args is not None
    except Exception as e:
        logging.info("proceed: User typed invalid command")
        logging.info(traceback.format_exc())
        return make_negative_response()

    if args.action == 'show_memes':
        return get_meme(channels=args.channels, limit=args.number, sort=args.sort)
    elif args.action == 'show_subscriptions':
        return get_subscriptions(recipient_id, limit=args.number, sort=args.sort)
    elif args.action == 'subscribe':
        return subscribe(recipient_id, channels=args.channels)
    elif args.action == 'unsubscribe':
        return unsubscribe(recipient_id, channels=args.channels)
    return make_negative_response()


def get_subreddit(reddit, subreddit='all', limit=1, sort='hot'):
    logging.info("get_subreddit: Subreddit {}, limit {}, sort {}".format(subreddit, limit, sort))
    if sort == 'hot':
        return reddit.subreddit(subreddit).hot(limit=limit)
    if sort == 'controversial':
        return reddit.subreddit(subreddit).controversial(limit=limit)
    if sort == 'top':
        return reddit.subreddit(subreddit).top(limit=limit)
    if sort == 'new':
        return reddit.subreddit(subreddit).new(limit=limit)
    if sort == 'gilded':
        return reddit.subreddit(subreddit).gilded(limit=limit)
    if sort == 'random_rising':
        return reddit.subreddit(subreddit).random_rising(limit=limit)
    if sort == 'rising':
        return reddit.subreddit(subreddit).rising(limit=limit)


def get_meme(channels=['all'], limit=1, sort='hot'):
    subreddit = "+".join(channels)
    reddit = praw.Reddit(client_id=keys['CLIENT_ID'],
                         client_secret=keys['CLIENT_SECRET'],
                         user_agent=keys['USER_AGENT'])
    # print(subreddit)
    text_response = []
    try:
        memes = []
        for submission in get_subreddit(reddit, subreddit=subreddit, limit=limit, sort=sort):
            memes.append(submission.url)
        text = ("Here are {} memes from '{}' channel:".format(len(memes), subreddit) 
               if len(memes) > 0 
               else "Unfortunately no memes on '{}' channel.")
        text_response.append(text)
        text_response += memes
        logging.info("get_meme: " + ''.join(text_response))
    except Exception as e:
        text_response.append("Problems accessing '{}' channel, probably you mistyped.".format(subreddit))
        logging.info("get_meme: " + traceback.format_exc())
    return text_response


def get_subscriptions(recipient_id, limit=1, sort='hot'):
    reddit = praw.Reddit(client_id=keys['CLIENT_ID'],
                         client_secret=keys['CLIENT_SECRET'],
                         user_agent=keys['USER_AGENT'])
    subscription_list = [str(x) for x in r.smembers(recipient_id)]

    text_response = []
    if len(subscription_list) == 0:
        logging.info("get_subscriptions: No subscriptions")
        text_response.append("You currently have no subscriptions. Subscribe to some channels.")
    for subreddit in subscription_list:
        logging.info("get_subscriptions: Subreddit {}".format(subreddit))
        key = '{}, {}, {}'.format(recipient_id, subreddit, sort)
        logging.info(key)
        last_viewed = [str(x) for x in r.lrange(key, 0 , -1)]
        logging.info("get_subscriptions: " + str(last_viewed))
        r.delete(key)
        try:
            memes = []
            new_last_viewed = []
            for submission in get_subreddit(reddit, subreddit=subreddit, limit=limit, sort=sort):
                r.lpush(key, submission.url)
                if submission.url not in last_viewed:
                    logging.info("get_subscriptions: " + submission.url)
                    memes.append(submission.url)
            text = ("Here are {} new memes from '{}' channel ('{}' sorting) since you've last viewed it:".format(len(memes) 
                if len(memes) < limit 
                else "many", 
                subreddit, sort) 
            if len(memes) > 0 
            else "Unfortunately no new memes on '{}' channel ('{}' sorting) since you've last viewed it.".format(subreddit, sort))
            text_response.append(text)
            text_response += memes
        except Exception as e:
            text_response.append("Problems accessing '{}' channel, probably you mistyped.".format(subreddit))
            logging.info("get_subscriptions: " + traceback.format_exc())
    return text_response


def subscribe(recipient_id, channels=['all']):
    reddit = praw.Reddit(client_id=keys['CLIENT_ID'],
                         client_secret=keys['CLIENT_SECRET'],
                         user_agent=keys['USER_AGENT'])
    subscribed_list = []
    for subreddit in channels:
        try:
            assert not r.sismember(recipient_id, subreddit)
            submissions = get_subreddit(reddit, subreddit=subreddit)
            subscribed_list.append(subreddit)
            r.sadd(recipient_id, subreddit)
            logging.info("subscribe: added subreddit {}".format(subreddit))
        except Exception as e:
            logging.info("subscribe: cannot add {}".format(subreddit))
            logging.info("subscribe: " + traceback.format_exc())
    text = ("Successfully subscribed to channels: '{}'. ".format("', '".join(subscribed_list)) + ("" 
            if len(subscribed_list) == len(channels)
            else "Others are inaccessible or you've already subscribed to them.")
        if len(subscribed_list) != 0
        else "Did not sunscribe to any channels." + ("" 
            if len(subscribed_list) == len(channels)
            else "They are inaccessible or you've already subscribed to them."))
    text_response = [text]
    return text_response


def unsubscribe(recipient_id, channels=['all']):
    reddit = praw.Reddit(client_id=keys['CLIENT_ID'],
                         client_secret=keys['CLIENT_SECRET'],
                         user_agent=keys['USER_AGENT'])
    if len(channels) == 0:
        logging.info("unsubscribe: No channels")
        text_response = ["No channels to unsunscribe."]
        return text_response
    unsubscribed_list = []
    for subreddit in channels:
        try:
            assert r.sismember(recipient_id, subreddit)
            unsubscribed_list.append(subreddit)
            r.srem(recipient_id, subreddit)
            logging.info("unsubscribe: deleted subreddit {}".format(subreddit))
        except:
            logging.info("unsubscribe: cannot delete {}".format(subreddit))
            logging.info("unsubscribe: " + traceback.format_exc())

    for subreddit in unsubscribed_list:
        for sort in sortings:
            key = '{}, {}, {}'.format(recipient_id, subreddit, sort)
            r.delete(key)
            logging.info("unsubscribe: " + key)
    text = ("Successfully unsubscribed from channels: '{}'. ".format("', '".join(unsubscribed_list)) + ("" 
            if len(unsubscribed_list) == len(channels)
            else "You've not subscribed to others.")
        if len(unsubscribed_list) != 0
        else "Did not unsunscribe from any channels." + ("" 
            if len(unsubscribed_list) == len(channels)
            else "You've not subscribed to them."))
    text_response = [text]
    return text_response


def make_negative_response(messages=[]):
    logging.info("make_negative_response: " + str(messages))
    return ["Invalid command!"] + messages + ["Try typing '--help'"]


if __name__ == "__main__":
    app.run()
