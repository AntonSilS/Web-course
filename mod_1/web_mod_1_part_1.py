from abc import abstractmethod, ABC
import pickle, json


class SerializationInterface(ABC):

    @abstractmethod
    def save_data(self):
        pass

    def get_data(self):
        pass
     
    

class JsonRecord(SerializationInterface):
    
    def __init__(self, filename = '', data = None):
        self.filename = filename
        self.data = data

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

    def get_data(self):
        with open(self.filename, 'r') as file:
            result = json.load(file)
            return result
    

class BinRecord(SerializationInterface):
    
    def __init__(self, filename = '', data = None):
        self.filename = filename
        self.data = data

    def save_data(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.data, file)
            
    def get_data(self):
        with open(self.filename, 'rb') as file:
            result = pickle.load(file)
            return result
        
if __name__ == "__main__":

    j = JsonRecord('data.json', [1, 2, 3, 4])
    j.save_data()
    print(f'from {j.__class__.__name__}: {j.get_data()}')

    b = BinRecord('data.bin', [1, 2, 3, 4])
    b.save_data()
    print(f'from {b.__class__.__name__}: {b.get_data()}')

