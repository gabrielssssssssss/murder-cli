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
        elementList = []
        for val in data.values():
            if val == None: 
                elementList.append(str("Non renseigné"))
            else: elementList.append(str(val))
        return ",".join(elementList)

    def yaml_prettier(self, data:dict, time:str) -> str:
        index = data["index"]
        path = f"./templates/{index}.yaml"
        with open(path, encoding="utf-8") as f:
            content = yaml.safe_load(f)

        fields = list(content["fields"])
        jsonTidy = self.json_tidy(data=data, order=fields)
        csvFormat = self.json_to_csv(data=jsonTidy)

        message = str(content["message"])
        for element in fields:
            frmt = "{" + element + "}"
            message = message.replace(frmt, str(jsonTidy[element]))

        message = message.replace("{csv_format}", str(csvFormat))
        message = message.replace("{time}", str(time))
        return message

