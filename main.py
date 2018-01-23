import praw
import sys
from colorama import init, Fore
import connection_manager
import ui_manager
from cmd_parser import CmdParser
import io_manager

def version():
    return 'pyreddit v0.1'

def get_cmd():
    sys.stdout.write(Fore.WHITE + '(pyreddit) > ')
    return raw_input()

def main():
    print 'Reading credentials from credentials.txt...'
    client_id, client_secret, user_agent, username, password = io_manager.load_credentials_from_file()
    print 'Read successfully!'

    print 'Connecting to reddit...'
    reddit = connection_manager.connect_to_reddit(client_id, client_secret, user_agent, username, password)
    #print 'Connection successful! Logged in as user', reddit.user.me()

    print 'Reading settings from settings.txt...'
    default_page_size, default_num_comments = io_manager.load_settings_from_file()
    print 'Read successfully!'

    print 'Startting pyreddit...'
    cmd_parser = CmdParser(reddit, default_page_size, default_num_comments)
    ui_manager.reset_screen(reddit)
    cmd_parser.cmd_help()

    while True:
        try:
            cmd_parser.parse_cmd(get_cmd())
        except SystemExit:
            quit()
        except Exception, e:
            print e

if __name__ == '__main__':
    init()
    main()
