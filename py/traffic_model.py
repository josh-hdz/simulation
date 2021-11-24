from agentpy import Model, AgentList, Space, AttrIter
from car_agent import CarAgent
from traffic_light import TrafficLightAgent
import json
import itertools
class TrafficModel (Model):

    def setup(self):
        cars_direction = AttrIter(
            (
                ([(0, 1)] * int(self.p['car']['amount'] * self.p['density'])) +\
                ([(0, -1)] * int(self.p['car']['amount'] * (1 - self.p['density'])))
            )
        )

        traffic_lights_direction = AttrIter([(0, -1),(0, 1)])

        # Generate car agents.
        self.cars = AgentList(
            self,
            self.p["car"]["amount"],
            CarAgent,
            direction=cars_direction
        )

        # Generates traffic lights agents
        self.traffic_lights = AgentList(
            self,
            self.p['traffic lights']['amount'],
            TrafficLightAgent,
            direction=traffic_lights_direction
        )

        # Generate space.
        self.intersection = Space(
            self,
            (self.p['a'], self.p['a']),
            torus=True
        )

        self.intersection.add_agents(self.cars, self._place_cars())
        self.intersection.add_agents(self.traffic_lights, self._place_traffic_lights())

    def step(self):
        self.traffic_lights.update()
        self.cars.update_position()
        self.cars.update_speed()

    def update(self):
        pass

    def end(self):
        pass 

    def _place_cars(self):
        # Next car's y cordenate in upstream lane.
        next_up_lane = 0.5 * self.p['a'] - self.p['b']
        # Next car's y cordenate in downstream lane.
        next_down_lane = 0.5 * self.p['a'] + self.p['b']
        # agent list index to separate car's in lanes.
        division_index = int(self.p["car"]["amount"] * self.p["density"])
        positions = []

        # Cars spwaned in upstream lane.
        for next_car in self.cars[0:division_index:]:
            positions.append(
                (
                    round(0.5 * (self.p['a'] + self.p['l']), 1),# X cordenate.
                    next_up_lane                                # Y cordenate.
                )
            )

            next_up_lane -= next_car.length + next_car.front_min_dist

        # Cars spawned in downstrem lane.
        for next_car in self.cars[division_index::]:
            positions.append(
                (
                    round(0.5 * (self.p['a'] - self.p['l']), 1),# X cordenate.
                    next_down_lane                              # Y cordenate.
                )
            )

            next_down_lane += next_car.length + next_car.front_min_dist
        
       
        print(len(positions))
        lst2 = [{'x':positions[i][0]/10,'z':positions[i][1]/10, 'id':i} for i in range(len(positions))]
        diccionario_codificado = json.dumps(lst2)
        print(diccionario_codificado)
        with open('data.json', 'w') as file:
            json.dump(lst2, file, indent=2)
        return positions

    def _place_traffic_lights(self):
        return [
            (
                0.5 * (self.p['a'] + self.p['l']),
                0.5 * self.p['a'] + self.p['b']
            ),
            (
                0.5 * (self.p['a'] - self.p['l']),
                0.5 * self.p['a'] - self.p['b']
            )
        ]