import json

from src import Report

json = json.loads(open("./src/values.json").read())
reports = []

for key, item in json['nodes'].items():
    print(key)
    reports.append(Report(item))

for report in reports:
    print("ID:   ", report.id)
    print("NAME:   ", report.name)
    for child in report.children:
        print(child.reason, " : ", child.value)
    for elem in report.elements:
        print("ELEMENT NAME:   ", elem.name)
        for data in elem.data:
            print("ELEMENT DATA ID:   ",data.id)
