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

class Magister(object):
	account_data = None

	def __init__(self, schoolprefix, username, password, stay_loggedin = False):
		self.schoolprefix = schoolprefix
		self.username = username
		self.password = password

		payload = {
			'Gebruikersnaam': username,
			'Wachtwoord': password,
			'IngelogdBlijven': str(stay_loggedin).lower()
		}

		with requests.Session() as s:
			s.post('https://' + str(schoolprefix) + '.magister.net/api/sessie', data = payload)
			self.account_data = json.loads(s.get('https://' + str(schoolprefix) + '.magister.net/api/account').text)