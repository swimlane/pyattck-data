import abc

from pyattck_data.generated import GeneratedData


class Base:

    generated_data = GeneratedData()

    def run(self):
        try:
            self.get()
        except:
            print('Failed running ')

    @abc.abstractmethod
    def get(self):
        pass
 