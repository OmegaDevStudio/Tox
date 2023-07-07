
from __future__ import annotations

import json
from typing import Any

import aiohttp

from .reports import Report


class Tox:
    def __init__(self, initial_value: int = 3) -> None:
        self.initial_value = initial_value
        self.picks: list[int] = [self.initial_value]
        self.elem_picks: list[str] = []
        self.reports: list[Report] = []
        self.json: Any = None
        self.message_link: str | None = None
        self.guild_id: str | None = None


    def load(self, report_type: str) -> Tox:
        if report_type == "message":
            self.message_link = input("Please input a message link [>] ")
        if report_type == "guild":
            self.guild_id = input("Please input a guild id [>] ")
        self.json = json.loads(open(f"./src/{report_type.lower()}.json").read())
        for _, item in self.json['nodes'].items():
            self.reports.append(Report(item))
        return self

    def show_options(self):
        for report in self.reports:
            if report.id == self.initial_value:
                print("here are your options:\n")
                report.show_children()

        while True:
        
            inp = input("\n\nPlease pick a value [>] ")

            try:
                inp = int(inp)
            except Exception:
                inp = str(inp)
            for report in self.reports: 
                if isinstance(inp, int):
                    if report.id == inp:
                        self.picks.append(inp)
                        try:
                            if len(report.children) > 0:
                                print("\nHere are your options")
                                print(report.header,"\n")
                                report.show_children()
                            elif next(elem for elem in report.elements if len(elem.data) > 0):
                                print("\nHere are your options")
                                print(report.header, "\n")
                                report.show_elements()
                            else:
                                print(f"Report Complete! You picked {self.picks}")
                                return
                        except StopIteration:
                            print(f"Report Complete! You picked {self.picks}")
                            return
                            
                else:
                    for elem in report.elements:
                        for data in elem.data:
                            if data.id == inp:
                                self.elem_picks.append(inp)
                                print(f"Report Complete! You picked {self.picks} and {self.elem_picks}")
                                return

    
    async def trigger(self, token: str):
        headers = {
            'Host': 'discord.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Authorization': token,
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwOS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzExNC4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE0LjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6Imh0dHBzOi8vZGlzY29yZC5jb20vIiwicmVmZXJyaW5nX2RvbWFpbiI6ImRpc2NvcmQuY29tIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjIxMDU2NiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=',
            'X-Discord-Locale': 'en-US',
            'X-Discord-Timezone': 'Europe/Bucharest',
            'X-Debug-Options': 'bugReporterEnabled',
            'Origin': 'https://discord.com',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': '__dcfduid=6c0f77d09af911ecbabc553e9df3c1ec; __sdcfduid=6c0f77d19af911ecbabc553e9df3c1ec3a133fb33af9a119e0e65e6e4d9c8566da36c361c58864808578756c89a34a86; __stripe_mid=04ffa3f5-6535-4f80-a731-9bd2b69957ce34cc80; _gcl_au=1.1.1160222537.1685451113; _ga_Q149DFWHT7=GS1.1.1685451113.1.0.1685451113.0.0.0; _ga=GA1.1.1770344604.1649958860; OptanonConsent=isIABGlobal=false&datestamp=Tue+May+30+2023+15%3A51%3A53+GMT%2B0300+(Eastern+European+Summer+Time)&version=6.33.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1&AwaitingReconsent=false&geolocation=RO%3BSV; __cfruid=89bb8b008575c05362859edeba3cc3892c56c1ad-1688727762; locale=en-US; __cf_bm=V61nFfJNfDFqqkpWa9zznXC0l2u.5Vge77WfP9Nu9iY-1688727766-0-AW+dejQju3K4IesQAZHhutuwZxq8j1IMH0xo2JdQ8WrMDMsny9JsSTb7vRluT1I88g==',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }
        async with aiohttp.ClientSession() as session:
            if self.message_link is not None:
                split = self.message_link.split("/")
                msg_id = split[-1]
                ch_id = split[-2]
                payload = {
                    "version":"1.0",
                    "variant":"3",
                    "language":"en",
                    "breadcrumbs":self.picks,
                    "elements":{},
                    "name":"message",
                    "channel_id":ch_id,
                    "message_id":msg_id
                }
                if len(self.elem_picks) > 0:
                    payload.update({"elements": {'pii_select':self.elem_picks}})
                url = 'https://discord.com/api/v9/reporting/message'
            elif self.guild_id is not None:
                payload = {
                    "version":"1.0",
                    "variant":"3",
                    "language":"en",
                    "breadcrumbs":self.picks,
                    "elements":{},
                    "name":"guild",
                    "guild_id": self.guild_id 
                }
                url = 'https://discord.com/api/v9/reporting/guild'
            async with session.post(url, headers=headers, json=payload) as resp:
                resp = await resp.json()
                print(resp)
    