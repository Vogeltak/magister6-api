"""
Copyright 2014 Maeb (and contributors)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import requests, json
from . import appointment, roosterwijziging, aanmelding, person

class Magister(object):
	account_data = None

	def __init__(self, schoolprefix, username, password, stay_loggedin = False):
		self.schoolprefix = schoolprefix
		self.username = username
		self.password = password
		self.__session = requests.Session()

		payload = {
			'Gebruikersnaam': username,
			'Wachtwoord': password,
			'IngelogdBlijven': str(stay_loggedin).lower()
		}

		with self.__session as s:
			res = s.post('https://{0}.magister.net/api/sessie'.format(schoolprefix), data = payload)
			if res.status_code == 403 and res.json()["Status"] == 1: raise Exception("Wrong username and/or password.")

			self.account_data = json.loads(s.get('https://{0}.magister.net/api/account'.format(schoolprefix)).text)

			id = self.account_data["Persoon"]["Id"]
			self.__person_url = "https://{0}.magister.net/api/personen/{1}".format(schoolprefix, id)
			self.__pupil_url = "https://{0}.magister.net/api/leerlingen/{1}".format(schoolprefix, id)

	def getAppointments(self, begin, end = None):
		"""
			Gets the appointments from Magister

			Parameters:
				begin - The start date of the appointments.
				end - Optional: The end date of the appointments.
		"""
		if end is None: end = begin

		def dateConvert(d): return "{0}-{1}-{2}".format(str(d.year).zfill(2), str(d.month).zfill(2), str(d.day).zfill(2))

		url = "{0}/afspraken?van={1}&tot={2}".format(self.__person_url, dateConvert(begin), dateConvert(end))
		with self.__session as s:
			return [appointment.Appointment.convert_raw(self, a) for a in s.get(url).json()["Items"]]

	# What is it in English?
	def getRoosterwijzigingen(self, begin, end = None):
		"""
			Gets the 'roosterwijzigingen' from Magister

			There will probably need to be an option to ask for 'roosterwijzigingen' for a specific day
		"""
		if end is None: 
			end = begin

		def dateConvert(d): return "{0}-{1}-{2}".format(str(d.year).zfill(2), str(d.month).zfill(2), str(d.day).zfill(2))

		url = "{0}/roosterwijzigingen?van={1}&tot={2}".format(self.__person_url, dateConvert(begin), dateConvert(end))
		with self.__session as s:
			return [roosterwijziging.Roosterwijziging.convert_raw(self, a) for a in s.get(url).json()["Items"]]

	def getAanmeldingen(self):
		"""
			Gets the aanmeldingen from Magister

		"""
		url = "{0}/aanmeldingen".format(self.__person_url)
		with self.__session as s:
			return [aanmelding.Aanmelding.convert_raw(self, a) for a in s.get(url).json()["Items"]]

	def getPersons(self, query, personType = None):
		"""
			Gets an List of Persons that matches the given profile.

			Paramters:
				query - The query the persons must match to (e.g: Surname, Name, ...). Should at least be 3 chars long.
				personType - The type the person must have. If none is given it will search for both Teachers and Pupils.
		"""
		if type(query) is not str or len(query) < 3: return []
		if personType is None: return self.getPersons(query, 3) + self.getPersons(query, 4)

		personType = {
			1: "Groep",
			3: "Docent",
			4: "Leerling",
			8: "Project"
		}.get(person.Person.convert_type(personType), "Overig")

		url = "{0}/contactpersonen?contactPersoonType={1}&q={2}".format(self.__person_url, personType, query)
		with self.__session as s:
			return [ person.Person.convert_raw(self, p) for p in s.get(url).json()["Items"] ]