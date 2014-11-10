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
