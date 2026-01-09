import os
import re

class Utils:
    def __init__(self):
        self.regex_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        self.regex_zip_code = r"^(?:0[1-9]|[1-8][0-9]|9[0-5]|97[1-9]|98[0-9])\d{3}$"
        self.regex_phone_number = r"^(?:0\d{9}|\+33\d{9})$"
        self.regex_birthdate = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{4})$"
    
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
            if re.search(self.regex_email, parse_element):
                dict_elements["email"] = {"value": parse_element, "operator": "OR"}
                dict_elements["email2"] = {"value": parse_element, "operator": "AND"}
            elif re.search(self.regex_zip_code, parse_element):
                dict_elements["zipcode"] = {"value": parse_element, "operator": "AND"}
            elif re.search(self.regex_phone_number, parse_element):
                dict_elements["mobile"] = {"value": parse_element, "operator": "OR"}
                dict_elements["mobile2"] = {"value": parse_element, "operator": "OR"}
                dict_elements["mobile3"] = {"value": parse_element, "operator": "AND"}
            elif re.search(self.regex_birthdate, parse_element):
                dict_elements["birthdate"] = {"value": parse_element, "operator": "AND"}
            else:
                if dict_elements.get("plain", "") == "":
                    dict_elements["plain"] = {"value": parse_element, "operator": "AND"}
                else:
                    dict_elements["plain"]["value"] = " ".join([dict_elements["plain"]["value"], parse_element])
        return dict_elements
                
    def strict_query_filter(self, dict_elements: dict) -> str:
        payload = []
        for key, values in dict_elements.items():
            if key == "plain":
                continue
            payload.append(f"{key}='{values.get('value')}'")
            payload.append(values.get("operator"))
        if payload != []:
            payload.pop()
        return " ".join(payload)
    
    def get_strict_values(self, elements: list) -> list:
        strict_elements = []
        for element in elements:
            element = str(element)
            if element.startswith("!") \
                or re.search(self.regex_birthdate, element) \
                or re.search(self.regex_phone_number, element) \
                or re.search(self.regex_email, element) \
                or re.search(self.regex_zip_code, element):
                    strict_elements.append(element.replace("!", ""))
        return strict_elements

    def check_strict_values(self, strict_elements:list, result:str) -> bool:
        for strict_element in strict_elements:
            strict_regex = re.compile(re.escape(r"{}".format(strict_element)), re.IGNORECASE)
            if bool(re.search(strict_regex, result)) != True:
                return False
        return True
