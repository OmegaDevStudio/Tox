import asyncio
import json

import aiohttp
import ujson

from src import Report

opt = input("Please input type of report.\nMessage\nGuild\n[>] ")
if opt.lower() == "message":
    json = json.loads(open("./src/message.json").read())
else:
    json = json.loads(open("./src/guild.json").read())
reports: list[Report] = []

def initial_load():
    for _, item in json['nodes'].items():
        reports.append(Report(item))
elem_picks = []
if opt.lower() == "message":
    picks = [3]
else:
    picks = [0]
def show_options():
    for report in reports:
        if opt.lower() == "message":
            if report.id == 3:
                print("here are your options:\n")
                report.show_children()
        else:
            if report.id == 0:
                print("here are your options:\n")
                report.show_children()

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
                        return picks

                    else:
                        print(f"Report Complete! You picked {picks}")
                        return picks
            else:
                for elem in report.elements:
                    for data in elem.data:
                        if data.id == inp:
                            elem_picks.append(inp)
                            print(f"Report Complete! You picked {picks} and {elem_picks}")
                            return picks, elem_picks


async def main():
    initial_load()
    show_options()
    token = 'tok'
    async with aiohttp.ClientSession(headers={'Authorization':token}, json_serialize=ujson.dumps) as session:
        x = await session.get('https://discord.com/api/v9/users/@me')
        if x.status == 401:
            print('Invalid token.')
        else:
            msg = input('Enter message link [>] ')
            msg_id = msg.split('/')[-1]
            ch_id = msg.split('/')[-2]
            report_payload = {
                "version":"1.0",
                "variant":"3",
                "language":"en",
                "breadcrumbs":picks,
                "elements":{'pii_select':elem_picks},
                "name":"message",
                "channel_id":ch_id,
                "message_id":msg_id
            }
            if opt.lower() == "message":
                tox = await session.post('https://discord.com/api/v9/reporting/message', json=report_payload)
            else:
                tox = await session.post('https://discord.com/api/v9/reporting/guild', json=report_payload)
            print(tox.status)
            xx = await tox.json()
            print(xx)
asyncio.run(main())
