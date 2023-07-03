import json

from src import Report

json = json.loads(open("./src/values.json").read())
reports: list[Report] = []

def initial_load():
    for _, item in json['nodes'].items():
        reports.append(Report(item))

def show_options():
    for report in reports:
        if report.id == 3:
            print("Here are your options:\n")
            report.show_children()
    elem_picks = []
    picks = [3]

    while True:
        inp = input("\n\nPlease pick a value [>] ")

        try:
            inp = int(inp)
        except Exception:
            inp = str(inp)

        for report in reports:

            if type(inp) == int:
                if report.id == inp:
                    picks.append(inp)
                    try:
                        if len(report.children) > 0:
                            print("\nHere are your options")
                            print(report.header,"\n")
                            report.show_children()
                            break
                        
                 
                        elif next(elem for elem in report.elements if len(elem.data) > 0):
                            print("\nHere are your options")
                            print(report.header, "\n")
                            report.show_elements()
                            break
                    except StopIteration:
                        print(f"Report Complete! You picked {picks}")
                        return

                    else:
                        print(f"Report Complete! You picked {picks}")
                        return
            else:
                for elem in report.elements:
                    for data in elem.data:
                        if data.id == inp:
                            elem_picks.append(inp)
                            print(f"Report Complete! You picked {picks} and {elem_picks}")
                            return
    
initial_load()
show_options()
