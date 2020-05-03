import json

message_content_types = {
    'text',
    'audio',
    'animation',
    'document',
    'game',
    'photo',
    'sticker',
    'contact'
}

class MessageFromUser:
    def __init__(self, source:dict):
        self.message_id = source['message_id']
        self.content_type = None
        self.command = None
        self.contact = None
        self.audio = None
        self.animation = None
        self.photo = None
        self.sticker = None
        self.game = None
        self.text = ''
        if 'text' in source:                
            self.text:str = source['text']
            self.content_type='text'
            if self.text.startswith('/'):
                # this is a comand
                command = self.text.split()[0].split('@')[0][1:] 
                self.command = command
        if 'audio' in source:
            self.content_type='audio'
            self.audio = source['audio']
        if 'animation' in source:
            self.content_type='animation'
            self.animation = source['animation']
        if 'document' in source:
            self.content_type='document'
            self.document = source['document']
        if 'game' in source:
            self.content_type='game'
            self.game = source['game']
        if 'photo' in source:
            self.content_type='photo'
            self.photo = source['photo']
        if 'sticker' in source:
            self.content_type='sticker'
            self.sticker = source['sticker']
        if 'contact' in source:
            self.content_type='contact'
            self.contact = source['contact']

class MessageToUser:
    def __init__(self, user, text=None, reply_markup=None, when=None, photo=None, document = None ,new_state=None):
        self.user = user
        self.message = {}
        if text: self.message['text'] = text
        if photo: self.message['photo'] = photo
        if document: self.message['document'] = document
        if reply_markup: self.message['reply_markup'] = reply_markup
        if new_state:
            self.new_state = new_state
        else: 
            self.new_state = None
        if when:
            self.when = when
        else: 
            self.when = None
        

class ReplyKeyboard:
    def __init__(self, remove_keyboard=False, resize_keyboard=False, one_time_keyboard=False, is_inline=False):
        self.rows=[[]]
        self.remove_keyboard = remove_keyboard
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.inline = is_inline
        pass
    
    def clear(self):
        self.rows = [[]]

    def add_button(self, name, row, request_contact=False, request_location=False, callback=None):
        button = {
            'text' : name,
            'request_contact' : request_contact,
            'request_location' : request_location
        }
        if self.inline and not callback is None:
            button['callback_data']=callback

        self.rows[row].append(button)
        pass

    def add_row(self):
        self.rows.append([])
        pass

    def to_json(self)->str:
        res = {
            'keyboard' : self.rows,
            'resize_keyboard' : True,
            'one_time_keyboard' : True,
            'remove_keyboard' : self.remove_keyboard
        }
        return json.dumps(res)
