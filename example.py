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

from magister import *
from datetime import datetime

school_prefix = input('School prefix: ')
username = input('Gebruikersnaam: ')
password = input('Wachtwoord: ')

m = magister.Magister(school_prefix, username, password)

print("Goedendag " + str(m.account_data['Persoon']['Roepnaam']))
print(m.appointments(datetime.now())[3].description)
