import os

class Utils:
    def __init__(self):
        pass
    
    def get_index_list(self) -> list:
        files = os.listdir("./templates")
        index_list = []
        for file in files:
            clean_file = file.replace(".yaml", "")
            index_list.append(clean_file)
        return index_list