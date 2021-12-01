from agentpy import Agent
import numpy as np
import math

class CarAgent (Agent):

    def setup(self, **kwargs):
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
        front_speed = 0
        traffic_light_dist = self.p['a']
        traffic_light_state = 0

        for car in self.model.cars:
            dist = self._get_front_dsit(car)

            if dist != -1 and dist < front_dist:
                front_dist = dist
                front_speed = car.speed

        for traffic_light in self.model.traffic_lights:
            dist = self._get_traffic_light_dist(traffic_light)

            if dist != -1 and dist < traffic_light_dist:
                traffic_light_dist = dist
                traffic_light_state = traffic_light.state

        # Actualiza la velocidad del auto
        if front_dist < 1:
            self.speed = 0
            self.state = 1
        elif front_dist < self.front_min_dist:
              self.speed = np.maximum(self.speed - 200*self.p['step time'], 0)

        elif front_dist < self.front_min_dist * 1.2:
              self.speed = np.maximum(self.speed - 100*self.p['step time'], 0)

        elif front_dist < self.front_min_dist * 1.5:
              self.speed = np.maximum(self.speed - 80*self.p['step time'], 0)

        elif traffic_light_state == 1 and traffic_light_dist < self.p['b'] * 2 + 10:
            self.speed = np.minimum(self.speed + 5*self.p['step time'], self.max_speed)

        elif traffic_light_state == 1 and traffic_light_dist < self.p['b'] * 2 + 50:
            self.speed = np.maximum(self.speed - 2*self.p['step time'], 0)
        
        elif traffic_light_state == 2 and traffic_light_dist < self.p['b'] * 2 + 10:
            self.speed = np.maximum(self.speed - 2*self.p['step time'], 0)

        elif traffic_light_state == 2 and traffic_light_dist < self.p['b'] * 2 + 50:
            self.speed = np.maximum(self.speed - 10*self.p['step time'], 0)

        else:
<<<<<<< HEAD
            self.speed = np.minimum(self.speed + 5 * self.p['step time'], self.max_speed)
=======
            self.speed = np.minimum(self.speed + 5 * self.p['step time'], self.max_speed) 
>>>>>>> 85a4236ac7bbec9edd6b35eee82f7036d563dfce

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
            return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2) - target.length / 2

        # Invalid distance.
        return -1

    def _get_traffic_light_dist(self, target):
        c = self.model.intersection.positions[self]
        t = self.model.intersection.positions[target]

        dp_direction = self._dot_product(
            target.direction,
            self.direction
        )
        
        dp_place = self._dot_product(
            (
                t[0] - c[0],
                t[1] - c[1]
            ),
            self.direction
        )

        if dp_direction < 0 and dp_place > 0:
            return math.sqrt((c[0] - t[0])**2 + (c[1] - t[1])**2)

        # Invalid target.
        return -1
    
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

 

    def _dot_product(self, v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]
