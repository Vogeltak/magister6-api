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

class Roosterwijziging(object):

	def __init__(self, magister):
		self.magister = magister

	def convert_raw(magister, raw):
		obj = Roosterwijziging(magister)
		
		obj.id = raw["Id"]
		obj.start = raw["Start"]
		obj.einde = raw["Einde"]
		obj.beginBySchoolHour = raw["LesuurVan"]
		obj.endBySchoolHour = raw["LesuurTotMet"]
		obj.fullday = raw["DuurtHeleDag"]
		obj.description = raw["Omschrijving"]
		obj.location = raw["Lokatie"]
		obj.status = raw["Status"]
		obj.type = raw["Type"]
		obj.displayType = raw["WeergaveType"]
		obj.content = raw["Inhoud"]
		obj.infoType = raw["InfoType"]
		obj.notes = raw["Aantekening"]
		obj.isDone = raw["Afgerond"]
		# --These are seperate objects--
		# obj.classes
		# obj.teachers
		# obj.classRooms
		# obj.groups
		obj.appointmentId = raw["OpdrachtId"]
		obj.hasAttachments = raw["HeeftBijlagen"]
		obj.attachments = raw["Bijlagen"]

		return obj
