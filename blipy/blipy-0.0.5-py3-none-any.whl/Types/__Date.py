class Date:
	@staticmethod
	def new(year, month, day, hour = 0, minute = 0, second = 0):
		twodigitnumber = lambda number: str(number).rjust(2, '0')
		month = twodigitnumber(month)
		day = twodigitnumber(day)
		hour = twodigitnumber(hour)
		minute = twodigitnumber(minute)
		second = twodigitnumber(second)
		return f'{year}-{month}-{day}T{hour}:{minute}:{second}.000Z'

	@staticmethod
	def interval(startDate, endDate):
		return {
			'startDate': startDate,
			'endDate': endDate
		}
