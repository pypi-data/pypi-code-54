class BaseDatatypeMapper(object):
    def __init__(self, datatype):
        self.datatype = datatype
        self.condition_type = self.datatype.condition_type

    def map(self, value):
        """return the value and its condition_type

        Mapping is done when converting the model into a form
        readable by DynamoDB. Mapping involves two steps.
        First it must return a dict of the value.
        Second it must "resolve" the value so DynamoDB can process it.
        ---
        ex) {"S": "Zac"}

        """
        if value == None:
            return {'NULL': True}
        res = {}
        res[self.condition_type] = self.resolve(value)
        return res

    def resolve(self, value):
        """returns the value resolved for dynamodb

        That is to say it is how the database expects
        it to be passed for all of the operations
        All classes that inherit from this class must implemenent
        a resolver.
        """
        return value

    def reconstruct(self, mapped_dict):
        """return the value from the mapped dict for model instantiation

        DynamoDB returns all attributes as a dict. Reconstructing
        reads this dict and "parses" the value. The return value
        can be used as the attribute on the Model.
        Reconstructing is only responsible for parsing the data
        as-is from DynamoDB. Default values are handled by the
        Datatype itself.
        """
        if mapped_dict.get('NULL') == True:
            return None
        return self.parse(mapped_dict[self.condition_type])

    def parse(self, value):
        """Convert the value from DynamoDB into a format for the Model

        This is the opposite of mapping. So when given
        {"S": "Zac"} it will return "Zac"
        value should never be None, reconstruct will not pass it here
        """
        return value
