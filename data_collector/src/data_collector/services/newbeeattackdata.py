from .base import Base


class NewBeeAttackDataset(Base):

    """
    Data Source: https://github.com/NewBee119/Attack-Technique-Dataset
    Author:  NewBee119

    This class is a wrapper for the above data set
    """
    URL = 'https://raw.githubusercontent.com/NewBee119/Attack-Technique-Dataset/master/tech_refer.json'

    def __get_data(self):
        return self.session.get(self.URL).json()

    def parse(self):
        self.count = 0
        return_dict = {}
        for key,val in self.__get_data().items():
            for item in val:
                if item not in return_dict:
                    return_dict[item] = []
                return_dict[item].append(key)
        for key,val in return_dict.items():
            technique = self.helper.get_object_by_external_id(key, "attack-pattern")
            if technique:
                technique.external_reference.extend(val)
                self.helper.replace_object(technique)
                self.count += 1
        self.__logger.info(f"Added {self.count} commands from {self.URL}")
