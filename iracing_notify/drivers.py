import pickle
from pathlib import Path
from driver import Driver

class Drivers:
    save_path = Path('data/drivers')

    def __init__(self):
        self.drivers = {}

    def update(self, driver_status):
        for name, current_series in driver_status.items():
            if name not in self.drivers:
                self.drivers[name] = Driver(name)
                
            self.drivers[name].next_state(current_series)
            

    @classmethod
    def load(cls):
        if cls.save_path.exists():
            with cls.save_path.open(mode='rb') as f:
                return pickle.load(f)
        else:
            cls.save_path.parent.mkdir(exist_ok=True)
            return Drivers()
    
    def save(self):
        with self.save_path.open(mode='wb') as f:
            pickle.dump(self, f)