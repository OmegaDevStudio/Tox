
class Report:
    def __init__(self, data) -> None:
        self._update(data)
        
    def __str__(self) -> str:
        return f"{self.name}   :   {self.id}"
    def _update(self, data):
        self.id = data['id']
        self.name = data['key']
        self.header = data['header']
        self.subheader = data['subheader']
        self.info = data['info']
        if data.get("elements") is not None:
            self.elements: list[Element] = [Element(data) for data in data['elements']]
        else:
            self.elements = []
        if len(data['children']) > 0:
            self.children: list[Children] = [Children(data) for data in data['children']]
        else:
            self.children = []
    
    def show_children(self):
        for child in self.children:
            print(f"        [ {child.reason} ]   :   {child.value}")

    def show_elements(self):
        for elem in self.elements:
            for data in elem.data:
                print(f"        [ {data.description} ]   :   {data.id}")


class Element:
    def __init__(self, data) -> None:
        self._update(data)

    def _update(self, data):
        self.name = data.get('name')
        self.type = data.get('type')
        if data.get('data') is not None:
            self.data: list[Element_data] = [Element_data(data) for data in data['data']] 
        else:
            self.data = []

class Element_data:
    def __init__(self, data) -> None:
        try:
            self.id = data[0]
            self.description = data[1]
            self.fake_val = None
        except IndexError:
            self.id = None
            self.description = None
            self.fake_val = None

class Children:
    def __init__(self, data) -> None:
        try:
            self.reason = data[0]
            self.value = data[1]
        except IndexError:
            self.reason =None
            self.value = None
