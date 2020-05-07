import re, sys


class Operations(object):

    def __init__(self):
        pass

    def IsNumber(self, num):
        try:
            pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
            result = pattern.match(num)
            if result:
                return True
            else:
                return False
        except:
            e = sys.exc_info()
            return False

    def BasicCalculation(self, operator, firstNumebr, secondNumber):
        switcher = {
            '+': firstNumebr + secondNumber,
            '-': firstNumebr - secondNumber,
            '*': firstNumebr * secondNumber,
            '/': firstNumebr / secondNumber
        }

        return switcher.get(operator, 0)

    def Coalesce(self, values):
        try:
            return str(next(filter(lambda r: (r != None and r != ''), values)))
        except:
            return '0'

    def Average(self, values):
        try:
            return str(sum(r for r in values if self.IsNumber(str(r))) / len(list(filter(lambda r: self.IsNumber(str(r)), values))))
        except:
            return ''
