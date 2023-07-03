import json

from src import Report

json = json.loads(open("./src/values.json").read())
reports: list[Report] = []

for key, item in json['nodes'].items():
    reports.append(Report(item))

for report in reports:
    print(f"{report}\n")
    print("CHILDREN:\n")
    report.show_children()
    print("ELEMENTS:\n")
    report.show_elements()
