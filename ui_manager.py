import praw
import os
from colorama import Fore

comment_counter = 0

def reset_screen(reddit):
    os.system('cls' if os.name == 'nt' else 'clear')
    print Fore.RED + '**' + Fore.WHITE + 'Logged in as user:', Fore.CYAN + str(reddit.user.me()), Fore.RED + '**', Fore.WHITE

def print_subreddit(reddit, subreddit):
    reset_screen(reddit)
    
    for i, submission in enumerate(subreddit):
        print Fore.WHITE + '--[', Fore.RED + str(i), Fore.WHITE + ']----------------------'
        print Fore.GREEN + str(submission.score), Fore.WHITE +  ':', Fore.BLUE + submission.title
        print Fore.WHITE + str(submission.author), Fore.YELLOW + str(submission.num_comments) + ' comments', Fore.BLUE + 'URL:', Fore.CYAN + submission.url

def print_submission(reddit, submission, max_comments):
    global comment_counter
    reset_screen(reddit)

    print Fore.BLUE + submission.title, Fore.GREEN + str(submission.score)
    print Fore.CYAN + submission.url
    
    submission_bits = _split_text_body(submission.selftext, 100)
    for bit in submission_bits:
        print bit

    comment_counter = 0
    submission.comments.replace_more(limit=0)
    for comment in submission.comments:
        _print_comments(comment, '', max_comments)

def _print_comments(comment, tab, max_comments):
    global comment_counter
    
    comment_counter += 1
    if comment_counter > max_comments:
        return

    print Fore.CYAN + tab + Fore.BLUE + str(comment.author), Fore.GREEN + '[' + str(comment.score) + ']', Fore.WHITE + ':'

    to_print = comment.body.replace('\n', ' ')
    comment_bits = _split_text_body(to_print, 100)

    for bit in comment_bits:
        print Fore.CYAN + tab + Fore.WHITE + bit

    for reply in comment.replies:
        _print_comments(reply, tab + '  | ', max_comments)

def _split_text_body(body, blocksize):
    body_bits = []
    i = 0
    j = 0
    while i < len(body):
        j += 100
        if j > len(body):
            j = len(body)
        else:
            while j < len(body) and body[j] != ' ':
                j += 1
        body_bits.append(body[i:j])
        i = j + 1
    return body_bits
