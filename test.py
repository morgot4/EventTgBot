



class Car:

    def __init__(self, color, speed) -> None:
        self.color = color
        self._speed = speed
        self.is_active = False

    def run(self, time_s):
        if self.is_active:
            return ((self._speed / 3.6) * time_s) / 1000
        else:
            return None
    
    @property
    def engine_start(self):
        self.is_active = True

    @engine_start.setter
    def engine_start(self, s: bool):
        self.is_active = s

    def stop(self):
        self.is_active = False

    @property
    def speed(self):
        return self._speed
    


car = Car("red", 50)
car.speed = 12
car.engine_start
car.engine_start = True
print(car.run(13))