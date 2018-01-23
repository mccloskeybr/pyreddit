import sys
import praw

"""
main entry point into reddit, connects using OAuth certificate
"""
def connect_to_reddit(client_id, client_secret, user_agent, username, password):
    reddit = praw.Reddit(   client_id=client_id,
                            client_secret=client_secret,
                            user_agent=user_agent,
                            username=username,
                            password=password)
    return reddit

"""
attempts to connect to a subreddit given the subreddits name and a praw instance
"""
def connect_to_subreddit(reddit, subreddit_title, tab):
    if tab == 'hot':
        return reddit.subreddit(subreddit_title).hot()
    elif tab == 'controversial':
        return reddit.subreddit(subreddit_title).controversial()
    elif tab == 'new':
        return reddit.subreddit(subreddit_title).new()
    elif tab == 'rising':
        return reddit.subreddit(subreddit_title).rising()
    else:
        return reddit.subreddit(subreddit_title).top()

