
settings_filename = './settings.txt'
credentials_filename = './credentials.txt'

def load_credentials_from_file():
    global credentials_filename
    f = open(credentials_filename, 'r')
    client_id = ''
    client_secret = ''
    user_agent = ''
    username = ''
    password = ''

    for line in f:
        line_bits = line.split('=')
        if line_bits[0] == 'default_client_id':
            client_id = line_bits[1][:-1]               # include [:-1] to get rid of included \n
        elif line_bits[0] == 'default_client_secret':
            client_secret = line_bits[1][:-1]
        elif line_bits[0] == 'default_user_agent':
            user_agent = line_bits[1][:-1]
        elif line_bits[0] == 'default_username':
            username = line_bits[1][:-1]
        elif line_bits[0] == 'default_password':
            password = line_bits[1][:-1]
        else:
            raise Exception('Unexpected token <' + line_bits[0] + '> recieved when reading from credentials file.')

    print 'a', 'b', 'c'
    print client_id, client_secret, user_agent, username, password

    if client_id == '' or client_secret == '' or user_agent == '' or username == '' or password == '':
        raise Exception('Error reading from credentials file.')

    return client_id, client_secret, user_agent, username, password

def load_settings_from_file():
    global settings_filename
    f = open(settings_filename, 'r')
    default_page_size = -1
    default_num_comments = -1

    for line in f:
        line_bits = line.split('=')
        if line_bits[0] == 'default_page_size':
            default_page_size = int(line_bits[1])
        elif line_bits[0] == 'default_num_comments':
            default_num_comments = int(line_bits[1])
        else:
            raise Exception('Unexpected token <' + line_bits[0] + '> recieved when reading from settings file.')

    if default_page_size == -1 or default_num_comments == -1:
        raise Exception('Error reading from settings file.')

    return default_page_size, default_num_comments

