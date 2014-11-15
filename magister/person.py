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

class Person(object):
	def __init__(self, magister, person_type, first_name, last_name):
		self.magister = magister
		self._type = person_type
		self.first_name = first_name
		self.last_name = last_name

	@property
	def person_type(self):
		return Person.convert_type(self._type, False)
	@person_type.setter
	def person_type(self, value):
		self._type = Person.convert_type(value, True)

	def __to_magister(self):
		obj = {}

		obj["Id"] = self.id
		obj["Type"] = self._type
		obj["Voornaam"] = self.firstName
		obj["Achternaam"] = self.lastName
		obj["Tussenvoegsel"] = self.namePrefix
		obj["Naam"] = self.fullName
		obj["Omschrijving"] = self.description
		obj["Groep"] = self.group
		obj["Docentcode"] = self.teacherCode
		obj["Emailadres"] = self.emailAddress

		return obj

	@staticmethod
	def convert_type(original, magister_style = True):
		if magister_style:
			if type(original) is int:
				if original not in [1, 3, 4, 8]: raise Exception("Invalid value: \"{0}\".".format(original))
				return original

			else:
				res = {
					"group": 1,
					"teacher": 3,
					"pupil": 4,
					"project": 8
				}.get(original.lower(), None)

				if res is None: raise Exception("Invalid value: \"{0}\".".format(original))
				return res
		else:
			return {
				1: "group",
				3: "teacher",
				4: "pupil",
				8: "project"
			}.get(original, None)

	@staticmethod
	def convert_raw(magister, raw):
		obj = Person(magister, raw["Type"], raw["Voornaam"], raw["Achternaam"])

		obj.id = raw["Id"]
		obj.name_prefix = raw["Tussenvoegsel"]
		obj.full_name = raw["Naam"]
		obj.description = raw["Omschrijving"] if raw["Omschrijving"] is not None else raw["Naam"]
		obj.group = raw["Groep"]
		obj.teacher_code = raw.get("Docentcode", None)
		obj.email_address = raw["Emailadres"]

		return obj