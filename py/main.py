from traffic_model import TrafficModel

def main():
    param = {
        "car": {
            "amount": 20,
            "length range": (20, 30),
            "max vel range": (1.0, 2.0),
            "min dist range": (20.0, 30.0)
        },
        'traffic lights': {
            'amount': 4,
            'time yellow': 0.5,
            'time green': 1
        },
        'a': 1000,
        'b': 30,
        'l': 30,
        'steps': 20000, 
        'step time': 0.01,
        'density': (0.20, 0.42, 0.23, 0.15),
        'dead time': 0.3
    }

    model = TrafficModel(param)
    result = model.run()

if __name__ == "__main__":
    main()
