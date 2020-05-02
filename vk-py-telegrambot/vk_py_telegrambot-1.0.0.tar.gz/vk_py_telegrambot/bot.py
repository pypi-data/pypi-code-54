from vk_py_telegrambot import api
from vk_py_telegrambot import store
from vk_py_telegrambot import types
from vk_py_telegrambot import users

import re
import logging
logger = logging.getLogger('bot')

import time

def default_finaly_handler(bot, message, user):
    bot.reply(user=user,message={'text':'Прости, я не понимаю :)'})

def _test(_filter, message):

    if not message.content_type in _filter['content_types']:
        return False

    if 'commands' in _filter:
        if message.command in _filter['commands']: return True
    
    if 're_text' in _filter:
        if re.findall(_filter['re_text'],message.text):
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

    def __init__(self, name):
        self.name = name
        self._handlers=[]

    
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

            try:
                result = record[1](bot, message, user)
            except Exception as e:
                logger.info(e)
            if result:
                break
        
        if self.finaly_handler:
            self.finaly_handler(bot, message, user)
        else:
            logger.info('Состояние бота: {}, Не обработано сообщение {} от пользователя {}'.format(self.name, message, user))

    def on_state_set(self, bot, user):
        if self.state_set_handler:
            try:
                self.state_set_handler(bot, user)
            except Exception as e:
                logger.info(e)

    def on_state_fadeout(self, bot, user):
        if self.state_fadeout_handler:
            try:
                self.state_fadeout_handler(bot, user)
            except Exception as e:
                logger.info(e)

default_state = BotState('default')
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
    
    def _send_pending_messages(self):
    # Забираем отложенные сообщения и отправляем пользователям
        pending_messages = self.store.get_pending_messages()
        for message in pending_messages:
            print(message)
            pass
    def _check_for_state_events(self):
    # Смотрим в базе по каким пользователям наступило время сбрасывать статус    
        events = self.store.get_chats_with_expired_stages()
        for event in events:
            print(event)
            pass

    def _proceed_updates(self):
    # Обрабатываем обновления от бота
        updates = api.get_updates(self.token,offset=self.last_update_id+1)
        for ju in updates:
            self.store.save_message(ju)
            if 'message' in ju: 
                #разбираем что пришло
                message = types.Message(ju['message'])
                user = users.User(source=ju['message']['from'], store=self.store)
                #вызываем промежуточные обработчики
                for mw in self.mw_handlers:
                    mw(bot=self, message=message, user=user)

                #понимаем текущее состояние и обрабатываем по состоянию
                if user.state in self.states:
                    self.states[user.state].proceed_message(bot=self, message=message, user=user)
                else:
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

    def send_message(self, user, message, when=None, new_state=None,  reply_markup=None):
        """
            :when: - Дата и время, когда сообщение должно быть отправлено. если не заполнено отправляется немеделенно
            :new_state: - состоения в которое должен перейти чат после отправки
            :reply_markup: - клавиатура для ответа. Можно собрать руками, но проще используя класс  ReplyKeyboard
        """
        if when is None:
            # мы отправляем сообщение немедленно
            if 'text' in message:
                api.send_message(
                    token=self.token,
                    chat_id=user.chat_id,
                    text = message['text'],
                    reply_markup=reply_markup,
                )
                pass
            if 'photo' in message:
                pass
        else:
            # мы сохраняем сообщение в базе
            self.store.put_message_in_queue(
                chat_id=user.chat_id,
                message=message,
                when=when, 
                new_state=new_state,
                reply_markup=reply_markup,
            )

    def reply(self, user, message, reply_markup=None, new_state=None):
        if 'text' in message:
            api.send_message(
                    token=self.token,
                    chat_id=user.chat_id,
                    text = message['text'],
                    reply_markup=reply_markup
            )
        
        if not new_state is None: 
            if not new_state[0] in self.states: 
                logger.warn('Для пользователя {}({}) установлено состояние {} для которого нет описания. Это может быть проблемой'.format(user.name, user.chat_id, new_state[0]))
            else:
                self.states[new_state[0]].on_state_set(bot=self, user=user)
            
            user.set_new_state(new_state)