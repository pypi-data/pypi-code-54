import logging
from datetime import datetime
from datetime import timedelta
logger = logging.getLogger('chatbot')

try:
    import pymongo
except ImportError:
    logger.error("Can't import pymongo module. Check requirements.txt")
    exit(500)

from datetime import datetime 

"""
    SessionStore - хранилище данных для бота
"""
class SessionStore:
    def __init__(self):
        self.conn = pymongo.MongoClient()       
        self.db = self.conn['bot-session-store']
        self.sessions = self.db['sessions']
        self.pending_queue = self.db['pending_queue']
        logger.debug('Connection to mongoclinet estabished. We find {} sessions'.format(self.sessions.find().count()))

    def save_message(self, message):
        self.db['messages'].insert_one(message)

    def put_message_in_queue(self, message, when, new_state=None, reply_markup=None):
        if when < datetime.now():
            logger.warn('Попытка отправить отложенное сообщение которое уже просроченно')

        el = {
            'message' : message.message,
            'fire_date' : when,
            'chat_id' : message.user.chat_id,
            'new_state' : new_state[0],
            'new_state_ttl' : new_state[1],
            'is_active' : True,
            'reply_markup' : reply_markup,
        }
        self.pending_queue.insert_one(el)

    def get_pending_messages(self)->[dict]:
        query = {
            'fire_date':{ '$lte':datetime.now()},
            'is_active':True
        }
        update = {'$set':{'is_active':False}}

        queue = self.pending_queue.find_and_modify(query=query, update=update)
        
        if queue is None:
            queue=[]

        if type(queue)==dict: 
            return [queue]

        return queue

    def get_userdata_by_id(self, chat_id)->dict:
        """Получает значение переменных для чата"""
        
        user_data = {}
        try:
            query = self.sessions.find_one({"chat_id":chat_id})
            if query:
                logger.debug('Query to db with result {}'.format(query))
                user_data = query
            return user_data
        except Exception as identifier:
            print(identifier)        

        return user_data

    def save_userdata_by_id(self, chat_id, state, context, saved_states):
        ud = self.sessions.find_one({'chat_id':chat_id})

        if ud is None:
            ud = {'chat_id':chat_id}
        
        ud['state'] = state[0]
        ud['state_ttl'] = state[1]
        ud['context'] = context
        ud['saved_states'] = saved_states

        self.sessions.find_one_and_replace(filter={'chat_id':chat_id},replacement=ud)

    def save_new_state(self, chat_id, new_state, ttl):
        """Переводит чат в стадию. Стадия используется для контекстной переписки"""  
        query = {'chat_id':chat_id}
        ud = self.sessions.find_one(query)

        if ud is None:
           ud = {
               'chat_id' : chat_id,
               'state' : new_state,
               'state_ttl' : ttl
           } 
           self.sessions.insert_one(ud)
        else:
            self.sessions.find_one_and_update(
                filter=query,update={
                    '$set':{
                        'state':new_state, 
                        'state_ttl': ttl
                }})
             
        logger.debug('Для пользователя {} установлено новое состояние {} на срок {} секунд'.format(chat_id, new_state,ttl))

    def get_chats_with_expired_stages(self):
        exp_sessions = self.sessions.find({'state_ttl':{'$lte':datetime.now()}})
        if exp_sessions.count()==0:
            return []
        else:
            logger.debug('Нашли {} стадии время ожидания по которым истекло'.format(exp_sessions.count()))
            events = []
            for s in exp_sessions:
                logger.debug('  chat_id: {}, state: {}, ttl: {}'.format(s['chat_id'], s['state'], s['state_ttl']))
                event = {
                    'state':s['state'],
                    'chat_id':s['chat_id']
                }
                events.append(event)
                self.sessions.find_one_and_update(
                    filter={'_id':s['_id']},
                    update={'$set':{
                        'state':None,
                        'state_ttl':None
                }})
            
            return events
        pass

    def __del__(self):
        if self.db:
            self.conn.close()
            self.conn = None
            self.db = None
            logger.debug('mongoclient was shuting down....')