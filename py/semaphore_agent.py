from agentpy import Agent


class SemaphoreAgent(Agent):

    def setup(self):
        # Declaracion de variables
        self.state = 0
        self.state_time = 0
        self.simulation_time = 0.1
        self.green = 30
        self.yellow = 5
        self.red = 20
        self.direction = [0, 1]

    def update(self):
        # Actualizar el semaforo
        self.state_time += self.simulation_time

        if self.state == 0: # Luz verde
            if self.state_time >= self.green:
                self.state = 1
                self.state_time = 0
        elif self.state_time == 1: # Luz amarilla
            if self.state_time >= self.yellow:
                self.state = 1
                self.state_time = 0
        elif self.state == 2:
            if self.state_time >= self.red: # Luz roja
                self.state = 0
                self.state_time = 0

    def green_light(self): #Poner el semaforo de color verde
        self.state = 0
        self.state_time = 0
    
    def yellow_light(self): #Poner el semaforo de color amarillo
        self.state = 1
        self.state_time = 0
    
    def red_light(self): #Poner el semaforo de color rojo
        self.state = 2
        self.state_time = 0