from agentpy import Agent
import numpy as np
import math

class CarAgent (Agent):

    def setup(self, **kwargs):
        self.step_time = self.p['step time']
        self.speed = 0.0
        self.direction = kwargs['direction']
        self.max_speed = self.model.random.uniform(
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

    def update_speed(self):
        front_dist = self.p['a']

        for car in self.model.cars:
            dist = self._get_front_dsit(car)

            if dist != -1:
                front_dist = dist

        # Actualiza la velocidad del auto

        if self.speed > 0:
            if front_dist < 2:
                self.speed = 0

            elif front_dist < 20:
                self.speed = np.maximum(self.speed - 200*self.step_time, 0)
            elif front_dist < 50:
                self.speed = np.maximum(self.speed - 80*self.step_time, 0)
        else:
            self.speed = 2

    def update_position(self):
        self.model.intersection.move_by(
            self,
            (self.direction[0] * self.speed, self.direction[1] * self.speed)
        )

    def _get_front_dsit(self, target):
        c1 = self.model.intersection.positions[self]
        c2 = self.model.intersection.positions[target]
        
        # Checks neighbor is in the same lane.
        dp_direction = self._dot_product(
            self.direction,
            target.direction
        )

        # Checks neighbor is in front.
        dp_place = self._dot_product(
            (
                c2[0] - c1[0],
                c2[1] - c1[1]
            ),
            self.direction
        )

        if dp_direction > 0 and dp_place > 0:
            return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

        # Invalid distance.
        return -1

    def _get_traffic_light_dist(self):
        pass
    
    # def move(self):
    #     intersec = self.model.intersection
    #     positions = intersec.positions
    #     front_dist = sys.maxsize if self.direction == 1 else -1

    #     # Find the car right in front.
    #     for neighbor in intersec.neighbors(self, self.length / 2 + 10):
    #         y_curr = positions[self][1]       # Y cordenate for this(self) car.
    #         y_neigh = positions[neighbor][1]  # Y cordenate for neighbor.

    #         # neighbor in the same lane
    #         if neighbor.direction == self.direction:
    #             # Upstream case with neighbor in front.
    #             if self.direction == 1 and y_neigh > y_curr:
    #                 dist = y_neigh - y_curr

    #                 if dist < front_dist:
    #                     front_dist = dist

    #             # Downstream case wiht neighbor in front.
    #             elif self.direction == 0 and y_neigh < y_curr:
    #                 dist = y_curr - y_neigh

    #                 if dist < front_dist:
    #                     front_dist = dist

    #     if self.velocity > 0:
    #         breaking_dist = (front_dist - self.front_min_dist)  / self.velocity

    #         if breaking_dist < front_dist:
    #             self._deaccelerate()
    #         elif breaking_dist > front_dist:
    #             self._accelerate()
    #     else:
    #         self._accelerate()

    #     intersec.move_by(self, (0, self.direction * self.velocity))

    def _accelerate(self):
        if self.velocity < self.max_speed:
            self.velocity += 1

    def _deaccelerate(self):
        if self.velocity > 0:
            self.velocity -= 1

    def _dot_product(self, v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]
