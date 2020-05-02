from vk_py_telegrambot import store

class User:
    chat_id:str
    name: str
    state: str
    context : dict
    store : store.SessionStore
    data : dict

    def __init__(self, source:dict, store:store.SessionStore):
        self.chat_id = source['id']
        if 'username' in source:
            self.name = source['username']
        else:
            self.name = source['first_name']
        self.store = store

        self.load()

    def load (self):
        ud = self.store.get_userdata_by_id(self.chat_id) 
        if 'context' in ud:
            self.context = ud['context']
        if 'state' in ud:
            self.state = ud['state']

    def save(self, store):
        pass

    def set_state(self, state):
        self.store.set_new_state(self.chat_id, state[0], state[1])
    
    def get_attr(self, attr):
        if attr in self.context: 
            return self.context[attr]
        else:
            return None
    
    def set_attr(self, attr, value):
        self.context[attr]=value

        if not self.store is None:
            self.store.set_locals_by_id(self.chat_id, self.context)

    def save_phone(self, phone_number):
        self.store.save_phone(chat_id=self.chat_id, phone=phone_number)
