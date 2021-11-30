from agentpy import Agent


class TrafficLightAgent(Agent):

    def setup(self, **kwargs):
        # Declaracion de variables
        self.state = 2
        self.state_time = 0
        self.green = self.p['traffic lights']['time green']
        self.yellow = self.p['traffic lights']['time yellow']
        self.red =self.p['traffic lights']['time red']
        self.direction = kwargs['direction']

    def update(self):
        # Actualizar el semaforo
        self.state_time += self.p['step time']

        if self.state == 0: # Luz verde
            if self.state_time >= self.green:
                self.state = 1
                self.state_time = 0
        elif self.state == 1: # Luz amarilla
            if self.state_time >= self.yellow:
                self.state = 2
                self.state_time = 0

    def calculate_traffic(self):
        traffic = 0
        start = sum(self.model.cars_per_dir[0:self.id - 1])
        end = start + self.model.cars_per_dir[self.id -1]

        # Iterate through neighbor cars in range.
        for car in self.model.cars[start:end]:

            # car is in the light's lane and before the light.
            if car._get_traffic_light_dist(self) != -1 and car.speed == 0:
                traffic += 1

        return traffic

    def green_light(self): #Poner el semaforo de color verde
        self.state = 0
        self.state_time = 0
    
    def yellow_light(self): #Poner el semaforo de color amarillo
        self.state = 1
        self.state_time = 0
    
    def red_light(self): #Poner el semaforo de color rojo
        self.state = 2
        self.state_time = 0