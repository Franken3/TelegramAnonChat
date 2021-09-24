import pandas as pd


def create_registration_dataBase():
    columns = ['username', 'chat_id', 'age', 'sex', 'reports', 'premium', 'companion', 'in_chat']
    data = []
    df = pd.DataFrame(data, columns=columns)
    df.set_index('username', inplace=True)
    df.to_csv(r'users.csv')


def create_queue_dataBase():
    columns = ['username']
    data = []
    df = pd.DataFrame(data, columns=columns)
    df.set_index('username', inplace=True)
    df.to_csv(r'inSearch.csv')


def registration(username, chat_id):
    df = pd.DataFrame(pd.read_csv('users.csv'))
    df.set_index('username', inplace=True)
    if username not in df.index:
        d = [{'username': username,
              'chat_id': chat_id,
              'age': None,
              'sex': None,
              'reports': 0,
              'premium': 0,
              'companin': None,
              'in_chat': False}]
        datf = pd.DataFrame.from_dict(d)
        datf.set_index('username', inplace=True)
        datf.to_csv('users.csv', mode='a', header=False)
        print(d)


def check_not_in_search(username: object) -> object:
    df = pd.DataFrame(pd.read_csv('inSearch.csv'))
    df.set_index('username', inplace=True)
    if f'{username}' not in df.index:
        return True
    else:
        return False


def add_in_search(username):
    d = [{'username': username}]
    df = pd.DataFrame.from_dict(d)
    df.set_index('username', inplace=True)
    df.to_csv('inSearch.csv', mode='a', header=False)


def search(username) -> object:
    df = pd.DataFrame(pd.read_csv('inSearch.csv'))
    users_df = pd.DataFrame(pd.read_csv('users.csv'))
    users_df.set_index('username', inplace=True)
    df.set_index('username', inplace=True)
    companion = None
    for companion in df.index:
        if username != companion:
            users_df.loc[username, 'in_chat'] = True
            users_df.loc[username, 'companion'] = companion
            users_df.loc[companion, 'in_chat'] = True
            users_df.loc[companion, 'companion'] = username
            users_df.to_csv('users.csv')
            del_from_search(username)
            del_from_search(companion)
            break
        else:
            print(f'Для {username} не найдено никого')
            companion = None
    return companion


def stop_chat(username):
    df = pd.DataFrame(pd.read_csv('users.csv'))
    df.set_index('username', inplace=True)
    try:
        companion = df.loc[username, 'companion']
        df.loc[username, 'in_chat'] = False
        df.loc[companion, 'in_chat'] = False
        df.loc[username, 'companion'] = None
        df.loc[companion, 'companion'] = None
    except:
        pass
    df.to_csv('users.csv')


def check_user_in_chat(username) -> object:
    df = pd.DataFrame(pd.read_csv('users.csv'))
    df.set_index('username', inplace=True)
    return df.loc[username, 'in_chat']


def del_from_search(username):
    df = pd.DataFrame(pd.read_csv('inSearch.csv'))
    df.set_index('username', inplace=True)
    df.drop(username, axis=0, inplace=True)
    df.to_csv(r'inSearch.csv')


def get_companin_username(username):
    df = pd.DataFrame(pd.read_csv('users.csv'))
    df.set_index('username', inplace=True)
    companion_username = df.loc[username, 'companion']
    return companion_username

def get_chat_id(username):
    df = pd.DataFrame(pd.read_csv('users.csv'))
    df.set_index('username', inplace=True)
    df.loc[username, 'chat_id']
    df.to_csv('users.csv')

def get_companion_chat_id(username):
    df = pd.DataFrame(pd.read_csv('users.csv'))
    df.set_index('username', inplace=True)
    companion_chat_id = int(df.loc[df.loc[username, 'companion'], 'chat_id'])
    return companion_chat_id

def reg_age_sex(username, age, sex):
    df = pd.DataFrame(pd.read_csv('users.csv'))
    df.set_index('username', inplace=True)
    df.loc[username, 'age'] = age
    df.loc[username, 'sex'] = sex
    df.to_csv('users.csv')

name = ['первый', 'второй', 'третий',
        'четвертый', 'пятый', 'шестой',
        'седьмой', 'восьмой', 'девятый', 'десятый']
name2 = 'единственный'

# for i in range(len(name)):
#    add_in_search(name[i], 1, 2)
