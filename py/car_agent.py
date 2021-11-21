from agentpy import Agent
import sys

class CarAgent (Agent):

    def setup(self, **kwargs):
        self.velocity = 0.0
        self.direction = kwargs['direction']
        self.max_velocity = self.model.random.uniform(
            self.p['car']['max vel range'][0],
            self.p['car']['max vel range'][1]
        )
        self.length = self.model.random.uniform(
            self.p['car']['length range'][0],
            self.p['car']['length range'][1]
        )
        self.front_min_dist = self.model.random.uniform(
           self.p['car']['min dist range'][0],
           self.p['car']['min dist range'][1]
        )

    def move(self):
        intersec = self.model.intersection
        positions = intersec.positions
        front_dist = sys.maxsize if self.direction == 1 else -1

        # Find the car right in front.
        for neighbor in intersec.neighbors(self, self.length / 2 + 10):
            y_curr = positions[self][1]       # Y cordenate for this(self) car.
            y_neigh = positions[neighbor][1]  # Y cordenate for neighbor.

            # neighbor in the same lane
            if neighbor.direction == self.direction:
                # Upstream case with neighbor in front.
                if self.direction == 1 and y_neigh > y_curr:
                    dist = y_neigh - y_curr

                    if dist < front_dist:
                        front_dist = dist

                # Downstream case wiht neighbor in front.
                elif self.direction == 0 and y_neigh < y_curr:
                    dist = y_curr - y_neigh

                    if dist < front_dist:
                        front_dist = dist

        if self.velocity > 0:
            breaking_dist = (front_dist - self.front_min_dist)  / self.velocity

            if breaking_dist < front_dist:
                self._deaccelerate()
            elif breaking_dist > front_dist:
                self._accelerate()
        else:
            self._accelerate()


        intersec.move_by(self, (0, self.direction * self.velocity))

    def _accelerate(self):
        if self.velocity < self.max_velocity:
            self.velocity += 1

    def _deaccelerate(self):
        if self.velocity > 0:
            self.velocity -= 1
