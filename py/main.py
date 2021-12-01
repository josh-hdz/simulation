from traffic_model import TrafficModel

def main():
    param = {
        "car": {
            "amount": 10,
            "length range": (2.5, 4.5),
            "max vel range": (1.0, 2.0),
            "min dist range": (3.0, 5.0)
        },
        'traffic lights': {
            'amount': 4,
            'time yellow': 0.5,
            'time green': 1
        },
        'a': 200,
        'b': 5,
        'l': 3.6,
        'steps': 1000, 
        'step time': 0.01,
        'density': (0.20, 0.42, 0.23, 0.15),
        'dead time': 0.3
    }

    model = TrafficModel(param)
    result = model.run()

if __name__ == "__main__":
    main()
