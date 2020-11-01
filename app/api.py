import random
import re
import os
import time

import requests
import vk_api
from flask import flash
from python3_anticaptcha import ImageToTextTask, errors

from app.utils import parse_accounts
from app.ANTICAPTCHA_TOKEN import ANTICAPTCHA_TOKEN


# def captcha_handler(captcha):
#     # TOKEN is not free, see `www.anticaptcha.com`
#     key = ImageToTextTask.ImageToTextTask(anticaptcha_key=ANTICAPTCHA_TOKEN, save_format='const') \
#             .captcha_handler(captcha_link=captcha.get_url())
#     # Пробуем снова отправить запрос с капчей
#     return captcha.try_again(key['solution']['text'])


def do_login(login, password, proxy=None):
    vk_session = vk_api.VkApi(login, password,
                              app_id=2685278,
                              scope=(vk_api.VkUserPermissions.MESSAGES |
                                     vk_api.VkUserPermissions.OFFLINE |
                                     vk_api.VkUserPermissions.PHOTOS),
                              )     # captcha_handler=captcha_handler

    if proxy:
        vk_session.http.proxies = {'http': 'http://' + proxy,
                                   'https': 'https://' + proxy}

    print('Logging into', login, password, end='')

    try:
        vk_session.auth(token_only=True, reauth=True)
    except vk_api.AuthError as e:
        print('... ERROR', e)
        return
    except requests.exceptions.ProxyError as e:
        print('... ERROR PROXY', e, proxy)
    except Exception as e:
        print('... ERROR AUTH', e)

    print('... SUCCESS')

    return vk_session, vk_session.get_api().users.get()[0]['id']


def get_sessions(accounts):
    sessions = {}

    for i, acc in enumerate(parse_accounts(accounts)):
        sessions[i] = do_login(acc[0], acc[1], acc[2])

    if len(sessions) == 1:
        return sessions[0]

    return sessions


def send_message(session, user_id, message, attachment=None, forward=None):
    func = session.get_api().messages.send
    kwargs = {'user_id': int(user_id),
              'message': message,
              'random_id': random.randint(-9223372036854775807, 9223372036854775807),
              'attachment': attachment,
              'forward_messages': forward}
    for sleep_time in range(30, 301, 30):
        try:
            return func(**kwargs)
        except vk_api.exceptions.Captcha as e:
            print('####################################')
            print(f'CaptchaError occured in message to {user_id}, recovering during {sleep_time} secs...')
            print('####################################', end='\n\n')    
            time.sleep(sleep_time)
    return func(**kwargs)



def get_photo_attachment(session, url):
    upload = vk_api.VkUpload(session)

    img_data = requests.get(url).content
    img_name = url.split('/')[-1]

    with open(img_name, 'wb') as handler:
        handler.write(img_data)

    photo = upload.photo_messages(img_name)

    vk_photo_url = 'photo{}_{}'.format(
        photo[0]['owner_id'], photo[0]['id']
    )

    if os.path.exists(img_name):
        os.remove(img_name)
    else:
        print("The file does not exist")

    return vk_photo_url


def get_attachments(session, msg):
    forward_pattern = re.compile(r"#forward\((.*)\)#")
    photo_pattern = re.compile(r"(.*)#photo\((.*)\)#")

    forward = forward_pattern.findall(msg)
    photo = photo_pattern.findall(msg)

    if forward:
        forward = [int(i) for i in forward[0].split(',')]
        msg = ''

    if photo:
        a = photo[0]
        photo = get_photo_attachment(session, a[1])
        msg = a[0]

    return msg, forward, photo
