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

class Appointment(object):
	def __init__(self, magister):
		self.magister = magister

	@staticmethod
	def convert_raw(magister, raw):
		obj = Appointment(magister)

		obj.id = raw["Id"]
		obj.begin = parse(raw["Start"])
		obj.end = parse(raw["Einde"])
		obj.beginBySchoolHour = raw["LesuurVan"]
		obj.endBySchoolHour = raw["LesuurTotMet"]
		obj.fullDay = raw["DuurtHeleDag"]
		obj.description = raw["Omschrijving"]
		obj.location = raw["Lokatie"] if raw["Lokatie"] is not None else ""
		obj.status = raw["Status"]
		obj.type = raw["Type"]
		obj.displayType = raw["WeergaveType"]
		obj.content = raw["Inhoud"]
		obj.infoType = raw["InfoType"]
		obj.notes = raw["Aantekening"]
		obj.isDone = raw["Afgerond"]
		obj.classes = (c["Naam"] for c in raw["Vakken"]) if raw["Vakken"] is not None else []
		#obj.teachers = (Person._convertRaw(magisterObj, p) for p in raw["Docenten"]) if raw["Docenten"] is not None else []
		obj.classRooms = (c["Naam"] for c in raw["Lokalen"]) if raw["Lokalen"] is not None else []
		obj.groups = raw["Groepen"]
		obj.appointmentId = raw["OpdrachtId"]
		obj.attachments = raw["Bijlagen"]
		obj.url = "#{magisterObj._personUrl}/afspraken/#{obj.id}"
		obj.scrapped = raw["Status"] == 0

		return obj