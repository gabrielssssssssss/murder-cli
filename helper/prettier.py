import yaml

class Prettier:
    def __init__(self):
        pass
    
    def json_tidy(self, data:dict, order:list) -> dict:
        json = {}
        for ord in order:
            value = data.get(ord, "Non renseigné")
            if value == None: 
                json[ord] = "Non renseigné"
            else: json[ord] = value
        return json

    def json_to_csv(self, data:dict) -> str:
        element_list = []
        for val in data.values():
            if val == None: 
                element_list.append(str("Non renseigné"))
            else: element_list.append(str(val))
        return ",".join(element_list)
    
    def message_prettier(self, content:dict, fields:list[any], json_tidy:dict, csv_format:str, time:str) -> str:
        message = content["message"]
        values = {
            "csv_format": csv_format,
            "time": time,
        }
        for field in fields:
            values[field] = json_tidy[field]
        for key, value in values.items():
            message = message.replace(f"{{{key}}}", str(value))
        return message

    def yaml_prettier(self, data:dict, time:str) -> str:
        path = f"./templates/{data["index"]}.yaml"

        with open(path, encoding="utf-8") as f:
            content = yaml.safe_load(f)

        fields = list(content["fields"])
        json_tidy = self.json_tidy(data=data, order=fields)
        csv_format = self.json_to_csv(data=json_tidy)

        return self.message_prettier(content=content, fields=fields, json_tidy=json_tidy, csv_format=csv_format, time=time)

