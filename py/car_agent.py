from agentpy import Agent

class CarAgent (Agent):

    def setup(self):
        self.velocity = 0
        self.max_velocity = self.model.random.uniform(
            self.p['car']['max vel range'][0],
            self.p['car']['max vel range'][1]
        )
        self.length = self.model.random.uniform(
            self.p['car']['length range'][0],
            self.p['car']['length range'][1]
        )
        self.min_distance = self.model.random.uniform(
           self.p['car']['min distance range'][0],
           self.p['car']['min distance range'][1]
        )

    def move(self):
        pass