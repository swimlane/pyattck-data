import requests

from ..base import Base


class NewBeeAttackDataset(Base):

    """
    Data Source: https://github.com/NewBee119/Attack-Technique-Dataset
    Author:  NewBee119

    This class is a wrapper for the above data set
    """

    URL = 'https://raw.githubusercontent.com/NewBee119/Attack-Technique-Dataset/master/tech_refer.json'

    def __get_data(self):
        return requests.get(self.URL).json()

    def get(self):
        return_dict = {}
        for key,val in self.__get_data().items():
            for item in val:
                if item not in return_dict:
                    return_dict[item] = []
                return_dict[item].append(key)
        for key,val in return_dict.items():
            for item in val:
                self.generated_data.add_external_reference(
                    technique_id=key,
                    reference=item
                )
