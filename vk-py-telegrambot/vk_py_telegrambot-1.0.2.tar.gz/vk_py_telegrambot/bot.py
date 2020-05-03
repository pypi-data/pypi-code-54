from vk_py_telegrambot import api
from vk_py_telegrambot import store
from vk_py_telegrambot import types
from vk_py_telegrambot import users

import re
import logging

logger = logging.getLogger('bot')

from datetime import datetime
import time

def default_finaly_handler(bot, message, user):
    bot.send_message(
        message=types.MessageToUser(
            user=user,
            text='Прости, я не понимаю :)'))

def _test(_filter, message):

    if not message.content_type in _filter['content_types']:
        return False

    if 'commands' in _filter:
        if message.command in _filter['commands']: return True
    
    if 're_text' in _filter:
        if len(re.findall(_filter['re_text'],message.text))>0:
            return True
    if 'func' in  _filter:
        return _filter['func'](message)

    return False

class BotState:
    name : str
    state_set_handler : callable
    state_fadeout_handler : callable
    finaly_handler : callable
    _handlers : list

    def __init__(self, name, finaly_handler=None):
        self.name = name
        self._handlers=[]
        if finaly_handler is None:
            self.finaly_handler = default_finaly_handler
    
    def addHandler(self, handler, content_types=['text'], commands=None, func=None, re_text=None):
        _filter = { 'content_types' : content_types}
        if not commands is None: _filter['commands']=commands
        if not re_text is None: _filter['re_text']=re_text
        if not func is None: _filter['func']=func
        
        self._handlers.append((_filter, handler))
    
    def proceed_message(self, bot, message, user):
        for record in self._handlers:
            if not _test(record[0], message):
                continue
            result = False
            try:
                result = record[1](bot, message, user)
            except Exception as e:
                logger.error(e)
            if result:
                return
        
        if self.finaly_handler:
            self.finaly_handler(bot, message, user)
            logger.warn('Состояние бота: {}, Не обработано сообщение {} от пользователя {}'.format(self.name, message.text, user.chat_id))
        else:
            logger.warn('Состояние бота: {}, Не обработано сообщение {} от пользователя {}'.format(self.name, message.text, user.chat_id))

    def on_state_set(self, bot, user):
        if self.state_set_handler:
            try:
                self.state_set_handler(bot, user)
            except Exception as e:
                logger.error(e)

    def on_state_fadeout(self, bot, user):
        if self.state_fadeout_handler:
            try:
                self.state_fadeout_handler(bot, user)
            except Exception as e:
                logger.error(e)

default_state = BotState(None)
default_state.finaly_handler = default_finaly_handler

class Bot:

    def __init__(self, token:str, proxy={}, skip_pending:bool=False, num_threads:int=2):
        self.token = token
        self.store = store.SessionStore()
        self.last_update_id = 0
        self.skip_pending = skip_pending
        self.default_state = default_state
        self.states:dict = {} 
        self.mw_handlers = []   

        if not proxy is None:api.proxy=proxy

        self.jobs_queue = None
        self.running = False


    def add_state(self, state:BotState):
        if state.name in self.states:
            logger.warn('Состояние переопределяется {}. возможно это проблема'.format(state.name))

        self.states[state.name] = state

    def proceed_state_fadeout(self, user, state):
        if state in self.states:
            bot_state = self.states[state]
            bot_state.on_state_fadeout(bot=self, user=user)
        else:
            logger.warn('Вызван обработчик снятия статуса {} но такого статуса нет. возможно это проблема'.format(state))
    
    def _send_pending_messages(self):
    # Забираем отложенные сообщения и отправляем пользователям
        pending_messages = self.store.get_pending_messages()
        for message in pending_messages:
            
            print(message)
            pass
    def _check_for_state_events(self):
    # Смотрим в базе по каким пользователям наступило время сбрасывать статус    
        events = self.store.get_chats_with_expired_stages()
        for e in events:
            if e['state'] in self.states:
                user = users.User(id=e['chat_id'], store=self.store, bot=self)
                self.states[e['state']].on_state_fadeout(bot=self, user=user)
            else:
                logger.warn('Вызван обработчик снятия статуса {} но такого статуса нет. возможно это проблема'.format(e['state']))

    def _proceed_updates(self):
    # Обрабатываем обновления от бота
        updates = api.get_updates(self.token,offset=self.last_update_id+1)
        for ju in updates:
            self.store.save_message(ju)
            if 'message' in ju: 
                #разбираем что пришло
                message = types.MessageFromUser(ju['message'])
                user = users.User(id=ju['message']['from']['id'], store=self.store, bot=self)
                #вызываем промежуточные обработчики
                for mw in self.mw_handlers:
                    mw(bot=self, message=message, user=user)

                #понимаем текущее состояние и обрабатываем по состоянию
                if user.state in self.states:
                    self.states[user.state].proceed_message(bot=self, message=message, user=user)
                else:
                    logger.warn('Для состояния {}. нет обработчика. возможно это проблема'.format(user.state))
                    self.default_state.proceed_message(bot=self, message=message, user=user)

            self.last_update_id=ju['update_id']

    def start(self, none_stop=False, interval=0, timeout=20):
        logger.info('Started .......')
        self.running=True
        while self.running:
            try:
                logger.debug('Pull {}'.format(self.last_update_id))
                
                self._send_pending_messages()

                self._check_for_state_events()

                self._proceed_updates()

                time.sleep(timeout)
            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt received.")
                break
        logger.info('Stopped polling.')

    def stop(self):
        self.running=False
        logger.info("Bot was stopped")
        pass

    def send_message(self, message:types.MessageToUser):
        if message.when is not None and message.when > datetime.now():
            self.store.put_message_in_queue(message=message, when=message.when)
            return
        
        api.send_message(self.token, message.user.chat_id, message)
        if message.new_state is not None:
            message.user.set_state(message.new_state)
        