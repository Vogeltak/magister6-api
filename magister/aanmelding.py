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

class Aanmelding(object):

	def __init__(self, magister):
		self.magister = magister

	def convert_raw(magister, raw):
		obj = Aanmelding(magister)

		obj.id = raw["Id"]
		# Links is a sub object, TODO implement it correctly
		obj.leerling_id = raw["LeerlingId"]
		obj.start = raw["Start"]
		obj.einde = raw["Einde"]
		obj.lesperiode = raw["Lesperiode"]
		# Studie is a sub object, TODO implement it correctly
		# Groep is a sub object, TODO implement it correctly
		obj.profiel = raw["Profiel"]
		obj.profiel2 = raw["Profiel2"]
		obj.aan_bron_melden = raw["AanBrondMelden"]
