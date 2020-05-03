from vk_py_telegrambot import types
from datetime import datetime
from datetime import timedelta


class User:
    '''
    Пользователь бота. Пользователь возникает при получения сообщения от пользователя ботом
    chat_id:str - идентификатор чата
    name: str - имя пользователя (тянется из профиля пользователя)
    state: str - текущее состояние пользователя
    saved_states : list - список сохраненных состояний (если мы уходим)
    context : dict - сохраненные переменные пользователя (по аналогии с куками)
    store : store.SessionStore - абстрактное хранилище данных (для сокрытия механики работы с БД)
    bot : chatbot.Bot - бот (нужен для того что бы вызывать из пользователя методы)
    data : dict - хранилище данных для наполнения промежуточными обрабочиками
    '''
    data : dict

    def __init__(self, id, store, bot):
        self.chat_id = id
        self.store = store
        self.bot = bot
        self.saved_states:list = []
        self.state = None
        self.state_ttl = None
        self.context = {}
        self.restore()

    def push_state(self, newstate, flush_states=False):
        if newstate[1]==0:
            newstate[1]=24*60*60 #По умолчанию срок ожидания в худшем случае сутки

        if flush_states:
            self.saved_states = ()
        else: 
            self.saved_states.append((self.state, self.state_ttl))

        self.state = newstate[0]
        self.state_ttl = datetime.now()+timedelta(minutes=newstate[1])

        self.store.save_new_state(self.chat_id, newstate[0], newstate[1])

    def pop_state(self):
        self.bot.proceed_state_fadeout(user=self, state=self.state)
        if len(self.saved_states)>0: 
            self.state = None
            self.state_ttl = None
        else:
            self.state, self.state_ttl = self.saved_states.pop()
        
        self.store.save_new_state(self.chat_id,self.state, self.state_ttl)

    def set_state(self,newstate):
        self.bot.proceed_state_fadeout(user=self, state=self.state)
        self.state = newstate[0]
        self.state_ttl = datetime.now()+timedelta(minutes=newstate[1])
        self.store.save_new_state(self.chat_id,self.state, self.state_ttl)
    
    def reply(self, message):
        self.bot.send_message(message)

    def restore (self):
        ud = self.store.get_userdata_by_id(self.chat_id) 
        if 'context' in ud:
            self.context = ud['context']
        if 'state' in ud:
            self.state = ud['state']
            self.state_ttl = ud['state_ttl']
        if 'saved_states' in ud:
            for state in ud['saved_states']:
                self.saved_states.append(state['state'], state['ttl'])

    def save(self):
        saved_states = []
        for state in self.saved_states:
            saved_states.append({
                'state':state[0],
                'state_ttl':state[1]
            })
        self.store.save_userdata_by_id(chat_id=self.chat_id, state=(self.state, self.state_ttl), context=self.context, saved_states=saved_states)

    def __del__(self):
        self.save()
