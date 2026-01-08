import os
import re

class Utils:
    def __init__(self):
        self.email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        self.zip_code = r"^(?:0[1-9]|[1-8][0-9]|9[0-5]|97[1-9]|98[0-9])\d{3}$"
        self.phone_number = r"^(?:0\d{9}|\+33\d{9})$"
        self.birthdate = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{4})$"
    
    def get_index_list(self) -> list:
        files = os.listdir("./templates")
        index_list = []
        for file in files:
            clean_file = file.replace(".yaml", "")
            index_list.append(clean_file)
        return index_list
    
    def parse_elements(self, elements:list) -> dict:
        dict_elements = {}
        for value in elements:
            if re.search(self.email_regex, value):
                dict_elements["email"] = {"value": value, "operator": "OR"}
                dict_elements["email2"] = {"value": value, "operator": "AND"}
            elif re.search(self.zip_code, value):
                dict_elements["zipcode"] = {"value": value, "operator": "AND"}
            elif re.search(self.phone_number, value):
                dict_elements["mobile"] = {"value": value, "operator": "OR"}
                dict_elements["mobile2"] = {"value": value, "operator": "OR"}
                dict_elements["mobile3"] = {"value": value, "operator": "AND"}
            elif re.search(self.birthdate, value):
                dict_elements["birthdate"] = {"value": value, "operator": "AND"}
            else:
                dict_elements["plain"] = {"value": value, "operator": "AND"}
        return dict_elements
                
    def strict_query_filter(self, dict_elements:dict) -> str:
        payload_filter_list = []
        for key, values in dict_elements.items():
            if key != "plain":
                payload_filter_list.append(f"{key}='{values.get("value")}'")
                if list(dict_elements.keys())[-1] != key:
                    payload_filter_list.append(f" {values.get("operator")}")
        return " ".join(payload_filter_list)