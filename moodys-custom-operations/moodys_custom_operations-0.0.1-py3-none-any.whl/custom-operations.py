import re
import sys
from functools import reduce
import statistics
import numpy


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
            return False

    def BasicCalculation(self, operator, firstNumebr, secondNumber):
        switcher = {
            '+': firstNumebr + secondNumber,
            '-': firstNumebr - secondNumber,
            '*': firstNumebr * secondNumber,
            '/': firstNumebr / secondNumber
        }

        return switcher.get(operator, 0)

    def COALESCE(self, values):
        try:
            return str(next(filter(lambda r: (r != None and str(r).strip() != 'None' and str(r).strip() != ''), values)))
        except:
            return 'ERROR'

    def AVERAGE(self, values):
        try:
            return str(sum(float(r) for r in values if self.IsNumber(str(r))) / len(list(filter(lambda r: self.IsNumber(str(r)), values))))
        except:
            return 'ERROR'

    def AVERAGENA(self, values):
        try:
            listOfNonNumbers = [r for r in values if not self.IsNumber(str(r))]

            if len(listOfNonNumbers) == 0:
                return str(sum(float(r) for r in values if self.IsNumber(str(r))) / len(list(filter(lambda r: self.IsNumber(str(r)), values))))
            else:
                return 'ERROR'
        except:
            return 'ERROR'

    def SUM(self, values):
        try:
            return str(sum(float(r) for r in values if self.IsNumber(str(r))))
        except:
            return 'ERROR'

    def SUB(self, values):
        try:
            return str(reduce((lambda x, y: float(x) - float(y)), values))
        except:
            return 'ERROR'

    def MUL(self, values):
        try:
            return str(reduce((lambda x, y: float(x) * float(y)), values))
        except:
            return 'ERROR'

    def DIV(self, values):
        try:
            return str(reduce((lambda x, y: float(x) / float(y)), values))
        except:
            return 'ERROR'

    def MEDIAN(self, values):
        try:
            floatValues = [float(item)
                           for item in values if self.IsNumber(item)]

            return round(statistics.median(floatValues), 8)
        except:
            return 'ERROR'

    def IF(self, values):
        try:
            conditionalExpression = str(values[0]).strip()

            operatorsToCheck = '==|!=|and|or|not|in'
            splitedValues = re.split(operatorsToCheck, values[0])

            if len(splitedValues) > 1:
                for itemIndex in range(len(splitedValues)):
                    if bool(splitedValues[itemIndex].strip()) and not self.IsNumber(splitedValues[itemIndex].strip()):
                        formatedString = "'{}'".format(
                            splitedValues[itemIndex])
                        conditionalExpression = self.ReplaceStringWithoutQuote(
                            conditionalExpression, splitedValues[itemIndex], formatedString)

            calculatedValue = eval(conditionalExpression.replace(
                "^", "**").replace("!", "not "))

            if calculatedValue == True or calculatedValue == 'True':
                return str(values[1])
            else:
                return str(values[2])
        except:
            return 'ERROR'   

    def ReplaceStringWithoutQuote(self, originalString, oldString, newString):
        returnString = str(originalString)
        increasedPosition = 0

        allIndices = [item.start()
                      for item in re.finditer(oldString, originalString)]

        for index in allIndices:
            if index == 0 or originalString[index - 1] != "'":
                returnString = returnString[0:(index + increasedPosition)] + newString + \
                    returnString[((index + increasedPosition) +
                                  len(oldString)):]
                # If the search string is found, increase posintion by 2 (length of '')
                increasedPosition += 2

        return returnString

    def AND(self, values):
        try:
            result = ''

            for item in values:
                if not bool(result):
                    result = item
                else:
                    result = result + ' and ' + item

            return result
        except:
            return 'ERROR'

    def OR(self, values):
        try:
            result = ''

            for item in values:
                if not bool(result):
                    result = item
                else:
                    result = result + ' or ' + item

            return result
        except:
            return 'ERROR'

    def IN(self, functionParams):
        try:
            values = str(functionParams).split('|')
            valueToCheck = "'{0}'".format(values[0])
            valuesInCheck = str(values[1]).split(',')
            valuesInCheck = ["'{0}'".format(
                str(item).strip()) for item in valuesInCheck]

            if valueToCheck in valuesInCheck:
                return True
            else:
                return False
        except:
            return 'ERROR'

    def STDEV(self, values):
        try:
            validInputData = [float(item) for item in values if self.IsNumber(item)]

            return round(statistics.stdev(validInputData), 8)
        except:
            return 'ERROR'

    def PERCENTILE(self, values, calculatePercentile):
        try:
            floatValues = [float(item)
                           for item in values if self.IsNumber(item)]

            return round(numpy.percentile(floatValues, calculatePercentile), 8)
        except:
            return 'ERROR'