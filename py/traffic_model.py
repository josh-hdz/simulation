from agentpy import Model, AgentList, Space, AttrIter
from car_agent import CarAgent
from traffic_light import TrafficLightAgent
import json
class TrafficModel (Model):

    def setup(self):
        self.dead_time = 0.0
        self.car_file = open('./js/car_data.json', 'w')
        self.traffic_light_file = open('./js/traffic_light_data.json', 'w')
        self.history_file = open('./js/data.json', 'w')
        self.car_positions_history = {}
        self.traffic_light_state_hsitory = {}
        self.history = {}
        self.cars_per_dir = self._calc_cars_per_direction(4)

        cars_direction = AttrIter(
            # upstream.
            ([(0, 1)] * self.cars_per_dir[0]) +\
            # downstream.
            ([(0, -1)] * self.cars_per_dir[1]) +\
            # leftstream.
            ([(-1, 0)] * self.cars_per_dir[2]) +\
            # rightstream.
            ([(1, 0)] * self.cars_per_dir[3])
        )

        traffic_lights_direction = AttrIter(
            [
                (0, -1),    # controls upstream.
                (0, 1),     # controls downstream.
                (1, 0),     # controls leftstream.
                (-1, 0)     # controls rightstream.
            ]
        )

        # Generates traffic lights agents
        self.traffic_lights = AgentList(
            self,
            self.p['traffic lights']['amount'],
            TrafficLightAgent,
            direction=traffic_lights_direction
        )

        # Generate car agents.
        self.cars = AgentList(
            self,
            self.p["car"]["amount"],
            CarAgent,
            direction=cars_direction
        )

        # Generate space.
        self.intersection = Space(
            self,
            (self.p['a'], self.p['a']),
            torus=True
        )

        self.intersection.add_agents(self.cars, self._place_cars())
        self.intersection.add_agents(self.traffic_lights, self._place_traffic_lights())

        self.traffic_lights.calculate_waiting()
        self.next_green()

        self._record_car_data()
        self._record_traffic_light_data()
        

    def step(self):
        self.traffic_lights.update()
        if self._all_red():
            self.next_green()
        self.cars.update_position()
        self.cars.update_speed()

    def update(self):
        self._record_car_data()
        self._record_traffic_light_data()

    def end(self):
        json.dump(self.car_positions_history, self.car_file, indent=2)
        json.dump(self.traffic_light_state_hsitory, self.traffic_light_file, indent=2)
        self._record_data()
        json.dump(self.history, self.history_file, indent = 2)

    # Determiens whcih pair of traffic lights will change state to green based
    # on the amount of cars waiting the green light.
    def next_green(self):
        traffic = self.traffic_lights.calculate_traffic()
        token = [
            traffic[i] + wait * 2
            for i, wait in enumerate(self.traffic_lights.waiting)
        ]

        if self.dead_time <= 0.0:
            # More traffic in vertical lanes.
            if token[0] + token[1] > token[2] + token[3]:
                self.traffic_lights[0].green_light()
                self.traffic_lights[1].green_light()
                self.traffic_lights[0].green = 0.2 * max(traffic[0], traffic[1])
                self.traffic_lights[1].green = 0.2 * max(traffic[1], traffic[0])

            # More traffic in horizontal lanes.
            elif token[2] + token[3] > token[0] + token[1]:
                self.traffic_lights[2].green_light()
                self.traffic_lights[3].green_light()
                self.traffic_lights[2].green = 0.2 * max(traffic[2], traffic[3])
                self.traffic_lights[3].green = 0.2 * max(traffic[3], traffic[2])

            # Same traffic in vertical and horizontal lanes.
            else:
                chosen = self.random.choices([(0,1), (2,3)], [0.5, 0.5])[0]

                self.traffic_lights[chosen[0]].green_light()
                self.traffic_lights[chosen[1]].green_light()

            self.dead_time = self.p['dead time']

        else:
            self.dead_time -= self.p['step time']

    # Calculates how many cars will be placed to each lane depending on its
    # direction and the lane density.
    def _calc_cars_per_direction(self, num_directions):
        leftover = 0
        cars_per_dir = []

        for i in range(num_directions):
            cars_in_dir = self.p['car']['amount'] * self.p['density'][i]

            leftover += cars_in_dir - int(cars_in_dir)

            cars_per_dir.append(int(cars_in_dir))

        for _ in range(int(leftover)):
            cars_per_dir[self.random.randint(0, num_directions - 1)] += 1

        return cars_per_dir

    # Returns a tuples' lsit with the initial x and y cordenates for all cars
    def _place_cars(self):
        # Next car's y cordenate in upstream lane.
        next_up_lane = 0.5 * self.p['a'] - self.p['b']
        # Next car's y cordenate in downstream lane.
        next_down_lane = 0.5 * self.p['a'] + self.p['b']
        # Next car's x cordenate in leftstream lane.
        next_left_lane = 0.5 * self.p['a'] + self.p['b']
        # Next car's x cordenate in rightstream lane.
        next_right_lane = 0.5 * self.p['a'] - self.p['b']
        # index to start iterating the agent list.
        start = 0
        # index to stop iterating the agnet list.
        end = self.cars_per_dir[0]
        positions = []

        # Cars spwaned in upstream lane.
        for next_car in self.cars[start:end]:
            positions.append(
                (
                    0.5 * (self.p['a'] + self.p['l']),  # X cordenate.
                    next_up_lane - next_car.length      # Y cordenate.
                )
            )

            next_up_lane -= next_car.length + next_car.front_min_dist

        start = end
        end = start + self.cars_per_dir[1]

        # Cars spawned in downstrem lane.
        for next_car in self.cars[start:end]:
            positions.append(
                (
                    0.5 * (self.p['a'] - self.p['l']),  # X cordenate.
                    next_down_lane + next_car.length    # Y cordenate.
                )
            )

            next_down_lane += next_car.length + next_car.front_min_dist

        start = end
        end = start + self.cars_per_dir[2]

        # Cars spawned in leftstream lane.
        for next_car in self.cars[start:end]:
            positions.append(
                (
                    next_left_lane + next_car.length,   # X cordenate.
                    0.5 * (self.p['a']  + self.p['l'])  # Y cordenate.
                )
            )

            next_left_lane += next_car.length + next_car.front_min_dist

        start = end

        # Cars spawned in rightstream lane.
        for next_car in self.cars[start:]:
            positions.append(
                (
                    next_right_lane - next_car.length,   # X cordenate.
                    0.5 * (self.p['a']  - self.p['l'])   # Y cordenate.
                )
            )
            
            next_right_lane -= next_car.length + next_car.front_min_dist
       
        return positions

    # Returns a tuples' list with the initial x and y cordenates for all traffic litghts.
    def _place_traffic_lights(self):
        return [
            (   # Light controling upstream lane.
                0.5 * (self.p['a'] + self.p['l']),  # X cordenate.
                0.5 * self.p['a'] + self.p['b']     # Y cordenate.
            ),
            (   # Light controling downstream lane.
                0.5 * (self.p['a'] - self.p['l']),  # X cordenate.
                0.5 * self.p['a'] - self.p['b']     # Y cordenate
            ),
            (   # Light controling leftstream lane.
                0.5 * self.p['a'] - self.p['b'],    # X cordenate.
                0.5 * (self.p['a'] + self.p['l'])   # Y cordenate. 
            ),
            (   # Light controling rightstream lane.
                0.5 * self.p['a'] + self.p['b'],    # X cordenate.
                0.5 * (self.p['a'] - self.p['l'])   # Y cordenate.
            )
        ]
    def _record_data(self):
        self.history =[  
             
            {
                'amount': self.p['car']['amount'],
                'frames': self.p["steps"],
                'semAmount': self.p['traffic lights']['amount']
            }

        ]

    # Appends all car's x and z cordenates to a list.
    def _record_car_data(self):

        self.car_positions_history[len(self.car_positions_history)] =[  
             
                {
                    'x':self.intersection.positions[self.cars[i]][0] - self.p['a'] / 2,
                    'z':self.intersection.positions[self.cars[i]][1] - self.p['a'] / 2,
                    'id':i
                }
                for i in range(self.p['car']['amount'])

        ]

    # Appends all traffic lights' state to a list.
    def _record_traffic_light_data(self):
        self.traffic_light_state_hsitory[len(self.traffic_light_state_hsitory)] =[ 
            
                {
                    'state': self.traffic_lights[i].state,
                    'id': i
                }
                for i in range(self.p['traffic lights']['amount'])
        ]

    # Returns true when all traffic lights' state is 2 (red).
    def _all_red(self):
        for light in self.traffic_lights:
            if light.state != 2:
                return False

        return True
