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

from dateutil.parser import parse
from . import person, util

class Appointment(object):
	def __init__(self, magister):
		self.magister = magister

	@property
	def is_done(self): return self._is_done
	@is_done.setter
	def is_done(self, value):
		if self._is_done == value: return
		
		self._is_done = value

		with self.magister.__sesion as s: s.put(self.url, data = self.__to_magister())

	def __to_magister(self):
		obj = {}

		obj["Id"] = self.id
		obj["Start"] = util.to_utc_string(self.begin)
		obj["Einde"] = util.to_utc_string(self.end)
		obj["LesuurVan"] = self.begin_by_school_hour
		obj["LesuurTotMet"] = self.end_by_school_hour
		obj["DuurtHeleDag"] = self.full_day
		obj["Omschrijving"] = self.description
		obj["Lokatie"] = self.location
		obj["Status"] = self.status
		obj["Type"] = self.type
		obj["WeergaveType"] = self.display_type
		obj["Inhoud"] = self.content
		obj["InfoType"] = self.info_type
		obj["Aantekening"] = self.notes
		obj["Afgerond"] = self.is_done
		obj["Lokalen"] = [ { "Naam": c } for c in self.class_rooms ]
		obj["Docenten"] = [ p.__Person_to_magister() for p in self.teachers ]
		obj["Vakken"] = [ { "Naam": c } for c in self.classes ]
		obj["Groepen"] = self.groups
		obj["OpdrachtId"] = self.appointment_id
		obj["Bijlagen"] = self.attachments if self.attachments is not None else []

		return obj

	@staticmethod
	def convert_raw(magister, raw):
		obj = Appointment(magister)

		obj.id = raw["Id"]
		obj.begin = parse(raw["Start"])
		obj.end = parse(raw["Einde"])
		obj.begin_by_school_hour = raw["LesuurVan"]
		obj.end_by_school_hour = raw["LesuurTotMet"]
		obj.full_day = raw["DuurtHeleDag"]
		obj.description = raw["Omschrijving"]
		obj.location = raw["Lokatie"] if raw["Lokatie"] is not None else ""
		obj.status = raw["Status"]
		obj.type = raw["Type"]
		obj.display_type = raw["WeergaveType"]
		obj.content = raw["Inhoud"]
		obj.info_type = raw["InfoType"]
		obj.notes = raw["Aantekening"]
		obj._is_done = raw["Afgerond"]
		obj.classes = [c["Naam"] for c in raw["Vakken"]] if raw["Vakken"] is not None else []
		obj.teachers = [person.Person.convert_raw(self, p) for p in raw["Docenten"]] if raw["Docenten"] is not None else []
		obj.class_rooms = [c["Naam"] for c in raw["Lokalen"]] if raw["Lokalen"] is not None else []
		obj.groups = raw["Groepen"]
		obj.appointment_id = raw["OpdrachtId"]
		obj.attachments = raw["Bijlagen"]
		obj.url = "#{magisterObj._personUrl}/afspraken/#{obj.id}"
		obj.scrapped = raw["Status"] == 0

		return obj
