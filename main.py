import json

json = json.loads(open("./values.json").read())
reports = []

for key, item in json['nodes'].items():
    if "key" in item and "id" in item:
        reports.append({item['key']: item['id']})
    if "children" in item:
        val = reports.index({item['key']: item['id']})
        reports[val].update({"reasons": []})
        if len(item['children']) > 0:
            for child in item['children']:
                reports[val]['reasons'].append({"reason": child[0], "value": child[1]})
    if "elements" in item:
        val = reports.index({item['key']: item['id']})
        reports[val].update({"elements": []})
        if len(item['elements']) > 0:

print(reports)
