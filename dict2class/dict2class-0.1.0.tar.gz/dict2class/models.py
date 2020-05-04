import json


class DictClass:
    def __init__(self, dict_class):
        '''
        [summary]

        Args:
            dict_class ([type]): [description]
        '''
        self.__dict__ = dict_class
        
    def decode(self):
        return self.__dict__

    def to_json(self, fields=[]):
        '''
        Get a json representation of the object

        Args:
            fields (list, optional): List of fields to include,
                                     will return all if blank.
                                     Defaults to [].

        Returns:
            str: json representation of the object
        '''
        json_dict = {key: value
                     for key, value in self.__dict__.items()
                     if key in fields or fields == []}
        return json.dumps(json_dict, default=lambda x: x.decode())

