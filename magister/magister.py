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
from . import appointment

class Magister(object):
	account_data = None

	def __init__(self, schoolprefix, username, password, stay_loggedin = False):
		self.schoolprefix = schoolprefix
		self.username = username
		self.password = password
		self.__sesion = requests.Session()

		payload = {
			'Gebruikersnaam': username,
			'Wachtwoord': password,
			'IngelogdBlijven': str(stay_loggedin).lower()
		}

		with self.__sesion as s:
			s.post('https://{0}.magister.net/api/sessie'.format(schoolprefix), data = payload)
			self.account_data = json.loads(s.get('https://{0}.magister.net/api/account'.format(schoolprefix)).text)

			id = self.account_data["Persoon"]["Id"]
			self.__person_url = "https://{0}.magister.net/api/personen/{1}".format(schoolprefix, id)
			self.__pupil_url = "https://{0}.magister.net/api/leerlingen/{1}".format(schoolprefix, id)

	def appointments(self, begin, end = None):
		"""
			Get's the appointments from Magister

			Parameters:
				begin - The start date of the appointments.
				end - Optional: The end date of the appointments.
		"""
		if end is None: end = begin

		def dateConvert(d): return "{0}-{1}-{2}".format(str(d.year).zfill(2), str(d.month).zfill(2), str(d.day).zfill(2))

		url = "{0}/afspraken?van={1}&tot={2}".format(self.__person_url, dateConvert(begin), dateConvert(end))
		with self.__sesion as s:
			return [appointment.Appointment.convert_raw(self, a) for a in json.loads(s.get(url).text)["Items"]]