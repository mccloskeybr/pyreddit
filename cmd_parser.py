import praw
import sys
import webbrowser
import connection_manager
import ui_manager

"""
class to tokenize and parse commands
"""
class CmdParser:
    """
    standard init, takes in defaults loaded from io (done in main)
    as commands are parsed here, requires access to the core praw reddit instance
    """
    def __init__(self, reddit, default_page_size, default_num_comments):
        self.reddit = reddit
        self.subreddit = None
        self.submission = None
        self.current_page = []
        self.page_size = default_page_size
        self.num_comments = default_num_comments

    """
    print the help screen
    """
    def cmd_help(self):
        print '** Welcome to pyreddit **'
        print 'h, help\t\t\t\t\t-\tprint this screen.'
        print 'v, version\t\t\t\t-\tdisplay version and general pyreddit info.'
        print 's, subreddit <a> <b=hot> <c=' + str(self.page_size) + '>\t\t-\tconnect to subreddit <a>, with optional tab <b> (tabs listed below), <c> many posts.'
        print '\t\t\t\t\t\tno arguments will reprint the current subreddit.'
        print '\t\t\t\t\t\ttabs: hot, controversial, new, rising, top (default hot).'
        print 'n, next <a=' + str(self.page_size) + '>\t\t\t\t-\tload the next <a> many posts from the current subreddit.'
        print 'o, open <a> <b=' + str(self.num_comments) + '>\t\t\t-\topen post (index <a>) from current subreddit, with <b> many comments.'
        print 'url <a>\t\t\t\t\t-\topen the current post\'s url, or index <a>\'s (if given), under the current subreddit.'
        print 'q, quit\t\t\t\t\t-\tquits pyreddit'

    """
    print current version and dev info
    """
    def cmd_version(self):
        print 'pyreddit v.1.0 by Brendan McCloskey'
        print 'mccloskeydev.wordpress.com'

    """
    connect to a specified subreddit (with some additional parameters) using connection_manager
    """
    def cmd_subreddit(self, title, tab, page_size):
        self.subreddit = connection_manager.connect_to_subreddit(self.reddit, title, tab)
        self.cmd_next_page(page_size)
        ui_manager.print_subreddit(self.reddit, self.current_page)

    """
    view the next page of the current subreddit (iterates through subreddit and adds to page)
    """
    def cmd_next_page(self, page_size):
        self.current_page = []
        for i in range(page_size):
            self.current_page.append(self.subreddit.next())

    """
    open a specified post from the current subreddit by sending post info to ui_manager
    """
    def cmd_open(self, index, num_comments):
        if self.subreddit == None:
            raise Exception('Not currently connected to a subreddit.')
        self.submission = self.current_page[index]
        ui_manager.print_submission(self.reddit, self.submission, num_comments)

    """
    open the url of a specified post or the current post by using the webbrowser
    """
    def cmd_open_url(self, index=None):
        if index is not None:
            self.submission = self.current_page[index]
        elif self.submission == None:
            raise Exception('Not currently connected to a post.')
        webbrowser.open_new_tab(self.submission.url)

    """
    parses a given command. usually parses and sends to method above
    """
    def parse_cmd(self, raw_cmd):
        if raw_cmd == '':
            return

        cmd_tokens = raw_cmd.split()

        cmd = cmd_tokens[0]
        if cmd == 'h' or cmd == 'help':
            self.cmd_help()

        elif cmd == 'v' or cmd == 'version':
            self.cmd_version()

        elif cmd == 's' or cmd == 'subreddit':
            self.submission = None
            if len(cmd_tokens) == 1:
                if self.subreddit == None:
                    raise Exception('Not currently connected to a subreddit.')
                ui_manager.print_subreddit(self.reddit, self.current_page)
            elif len(cmd_tokens) == 2:
                self.cmd_subreddit(cmd_tokens[1], 'hot', self.page_size)
            elif len(cmd_tokens) == 3:
                self.cmd_subreddit(cmd_tokens[1], cmd_tokens[2], self.page_size)
            elif len(cmd_tokens) == 4:
                self.cmd_subreddit(cmd_tokens[1], cmd_tokens[2], int(cmd_tokens[3]))

        elif cmd == 't' or cmd == 'tab':
            self.cmd_tab(cmd_tokens[1])

        elif cmd == 'n' or cmd == 'next':
            self.submission = None
            if len(cmd_tokens) == 1:
                self.cmd_next_page(self.page_size)
            elif len(cmd_tokens) == 2:
                self.cmd_next_page(int(cmd_tokens[1]))
            ui_manager.print_subreddit(self.reddit, self.current_page)

        elif cmd == 'o' or cmd == 'open':
            num_comments = self.num_comments
            if (len(cmd_tokens) > 2):
                num_comments = int(cmd_tokens[2])
            self.cmd_open(int(cmd_tokens[1]), num_comments)

        elif cmd == 'url':
            if len(cmd_tokens) == 1:
                self.cmd_open_url()
            elif len(cmd_tokens) == 2:
                self.cmd_open_url(int(cmd_tokens[1]))

        elif cmd == 'q' or cmd == 'quit':
            print 'Closing ...'
            raise SystemExit

        else:
            raise Exception('Error parsing. Type \'h\' or \'help\' for help.')

