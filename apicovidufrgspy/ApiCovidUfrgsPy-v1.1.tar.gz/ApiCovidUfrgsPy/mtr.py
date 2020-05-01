import requests as r
import numpy as np

url = r.get('https://api-covid-ufrgs.herokuapp.com/links').json()[-1]['link']

class Municipios:
	def __init__(self, url=url):
		self.url = url + '/index/municipios'
		self.data = r.get(self.url).json()

	def matriz_municipios(self):
		d = self.data
		arr = []
		for mp in d:
			arr.append([mp['nome'], mp['pop_senso_2010'], mp['pop_est_2019'], mp['mesoregiao']])
		return np.asarray(arr)

class Distancias:
	def __init__(self,url=url):
		self.url = url + '/index/distancias'
		try:
			self.mps = r.get(self.url).json()
		except NameError as err:
			print(err);


	def matriz_distancia(self):
		arr_arr = []
		for i in range(0,167):
			arr = []
			for mp in self.mps[i*167:(i+1)*167]:
				arr.append(mp['distancia'])
			arr_arr.append(arr)
		return np.asarray(arr_arr)

	def matriz_limitrofes(self):
		arr_arr = []
		for i in range(0,167):
			arr = []
			for mp in self.mps[i*167:(i+1)*167]:
				if(mp['limitrofes'] == 1):
					arr.append(mp['distancia'])
				elif(mp['limitrofes'] == 0):
					arr.append(0)
			arr_arr.append(arr)
		return np.asarray(arr_arr)

	def matriz_distancia_raio(self, raio):
		arr_arr = []
		for i in range(0,167):
			arr = []
			for mp in self.mps[i*167:(i+1)*167]:
				if(mp['distancia'] <= raio):
					arr.append(mp['distancia'])
				else:
					arr.append(0)
			arr_arr.append(arr)
		return np.array(arr_arr)

class Rodoviarias:
	def __init__(self, url=url):
		self.url = url+'/index/rodoviarias/linhas'
		self.mps = r.get(self.url).json()

	def matriz_rodoviarias(self):
		arr_arr = []
		for i in range(0,167):
			arr = []
			for mp in self.mps[i*167:(i+1)*167]:
				arr.append(mp['quantidade'])
			arr_arr.append(arr)
		return np.asarray(arr_arr)
	def status(self):
		pass
	def detalhes(self):
		pass

class CovidStatus:
	def __init__(self, url=url):
		self.url = url + '/index/infectados'
		self.data = r.get(self.url).json()
	def matriz_infectados(self):
		d= self.data
		self.medicoes = int(len(self.data)/167)
		arr_arr = []
		for i in range(0,self.medicoes):
			arr = []
			for j in d[i*self.medicoes:(i+1)*self.medicoes]:
				arr.append(j['numero_infectados'])
			arr_arr.append(arr)

		return np.asarray(arr_arr)

	def matriz_obitos(self):
		pass

class Localizacao:
	def __init__(self,url=url):
		self.url = url + '/index/localizacao'
		self.data = r.get(self.url).json()

	def matriz_localizacao(self):
		arr = []
		arr_arr = []
		for d in self.data:
			arr.append(d['lat'])
			arr.append(d['lng'])
			arr_arr.append(arr)
			arr = []
		return np.asarray(arr_arr)



