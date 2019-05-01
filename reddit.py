# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('action', default='show_memes', choices=['show_memes', 'how_subsriptions', 'subscribe', 'unsubscribe'], help='What do you want to do?')
# parser.add_argument('--number', '-n', default=1, help='Number of memes to display')
# parser.add_argument('--sort', '-s', default='hot', choices=['controversial', 'hot', 'top', 'new', 'gilded', 'random_rising', 'rising'], help='Sorting of memes')
# parser.add_argument('--channels', '-c', default=['all'], nargs='*', help='Channels where to search memes')
# args = parser.parse_args('--help')
# args.number = int(args.number)
# assert isinstance(args.number, int)
# assert args.number > 0
# print(args)

# import json

# struct = {
#     'CLIENT_ID' : "qWPfdFhEfHwu6w",
#     'CLIENT_SECRET' : "29bEv_MSFuXqphuAwsfMjqSq4Ls",
#     'USER_AGENT' : "ubuntu:reddit_meme_bot:v1.0 (by /u/ogarokpeter)",
#     'ACCESS_TOKEN' : 'EAAEfm1od0ZAgBAEcQBrpFgEp2zaBNZBReElpIytYHjnwtFsASx7an6x1HnKlRTil0hmfJpssiymKufR19JVVx7PhXRW3UjAYfWeNke8L1DxH2sv3AZCnwmatkgMNZARzNKGZB3oFXdNGJFuyIWZB1gOnW1rRKQMpHeXZAN3lnsX1gZDZD',
#     'VERIFY_TOKEN' : 'FUCKING_TOKEN'
# }

# with open('keys', 'w') as f:
#     json.dump(struct, f)

sortings = list(range(1, 11))
print(
"""usage: [-h] 
                 [--sort {""" + ','.join([str(x) for x in sortings]) + """}]
                 [--channels [CHANNELS [CHANNELS ...]]]
                 {show_memes,show_subscriptions,subscribe,unsubscribe}
"""
)