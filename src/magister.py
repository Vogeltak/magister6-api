"""
Copyright 2014 Maeb

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

username = input('Gebruikersnaam: ')
password = input('Wachtwoord')

payload = {
	'Gebruikersnaam': username,
	'Wachtwoord': password,
	'IngelogdBlijven': 'false'
}

data_account = 	0
data_roosterwijzigingen = 0

with requests.Session() as s:
	s.post('https://theresia.magister.net/api/sessie', data=payload)

	data_account = json.loads(s.get('https://theresia.magister.net/api/account').text)

print("Goedendag " + str(data_account['Persoon']['Roepnaam']))
