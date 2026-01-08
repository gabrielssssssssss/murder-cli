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
            parse_element = str(value).replace("!", "")
            if re.search(self.email_regex, parse_element):
                dict_elements["email"] = {"value": parse_element, "operator": "OR"}
                dict_elements["email2"] = {"value": parse_element, "operator": "AND"}
            elif re.search(self.zip_code, parse_element):
                dict_elements["zipcode"] = {"value": parse_element, "operator": "AND"}
            elif re.search(self.phone_number, parse_element):
                dict_elements["mobile"] = {"value": parse_element, "operator": "OR"}
                dict_elements["mobile2"] = {"value": parse_element, "operator": "OR"}
                dict_elements["mobile3"] = {"value": parse_element, "operator": "AND"}
            elif re.search(self.birthdate, parse_element):
                dict_elements["birthdate"] = {"value": parse_element, "operator": "AND"}
            else:
                dict_elements["plain"] = {"value": parse_element, "operator": "AND"}
        return dict_elements
                
    def strict_query_filter(self, dict_elements:dict) -> str:
        payload_filter_list = []
        for key, values in dict_elements.items():
            if key != "plain":
                payload_filter_list.append(f"{key}='{values.get("value")}'")
                if list(dict_elements.keys())[-1] != key and len(list(dict_elements.keys())) != 2:
                    payload_filter_list.append(f" {values.get("operator")}")
        return " ".join(payload_filter_list)
    
    def get_strict_value(self, elements:list) -> list:
        strict_elements = []
        for element in elements:
            if str(element).startswith("!"):
                parse_element = str(element).replace("!", "")
                strict_elements.append(parse_element)
        return strict_elements

    def check_strict_value(self, elements:list, result:str) -> bool:
        strict_elements = self.get_strict_value(elements=elements)
        for strict_element in strict_elements:
            if strict_element in result:
                return True
        return False