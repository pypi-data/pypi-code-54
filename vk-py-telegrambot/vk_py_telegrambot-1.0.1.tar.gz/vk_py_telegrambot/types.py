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

class Message:
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

class ReplyKeyboard:
    def __init__(self):
        self.rows=[[]]
        self.remove_keyboard = False
        self.resize_keyboard = False
        self.one_time_keyboard = False
        pass
    
    def clear(self):
        self.rows = [[]]

    def add_button(self, name, row, request_contact=False,request_location=False):
        button = {
            'text' : name,
            'request_contact' : request_contact,
            'request_location' : request_location
        }
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
