from agentpy import Model, AgentList, Space
from car_agent import CarAgent

class TrafficModel (Model):

    def setup(self):

        # Generate agents.
        self.agents = AgentList(
            self,
            self.p["car"]["amount"],
            CarAgent,
        )

        # Generate space.
        self.intersection = Space(self, (self.p['a'], self.p['a']))

        self.intersection.add_agents(self.agents, self._init_cars_loc())

    def step(self):
        self.agents.move()

    def update(self):
        pass

    def end(self):
        pass 

    def _init_cars_loc(self):
        # Next car's y cordenate in upstream lane.
        next_up_lane = 0.5 * self.p['a'] - self.p['b']
        # Next car's y cordenate in downstream lane.
        next_down_lane = 0.5 * self.p['a'] + self.p['b']
        # agent list index to separate car's in lanes.
        division_index = int(self.p["car"]["amount"] * self.p["density"])
        positions = []

        # Cars spwaned in upstream lane.
        for next_car in self.agents[0:division_index:]:
            positions.append(
                (
                    round(0.5 * (self.p['a'] + self.p['l']), 1),# X cordenate.
                    next_up_lane                                # Y cordenate.
                )
            )

            next_up_lane -= next_car.length + next_car.front_min_dist

        # Cars spawned in downstrem lane.
        for next_car in self.agents[division_index::]:
            positions.append(
                (
                    round(0.5 * (self.p['a'] - self.p['l']), 1),# X cordenate.
                    next_down_lane                              # Y cordenate.
                )
            )

            next_down_lane += next_car.length + next_car.front_min_dist

        return positions