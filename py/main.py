from traffic_model import TrafficModel

def main():
    param = {
        "car": {
            "amount": 8,
            "length range": (2.5, 4.5),
            "max vel range": (10.0, 16.67),
            "min dist range": (3.0, 5.0)
        },
        'traffic lights': {
            'amount': 2,
            'time red': 2,
            'time yellow': 2,
            'time green': 2
        },
        'a': 500,
        'step time': 0.1,
        'b': 5,
        'l': 3.6,
        "density": 0.5,
        'steps': 1000,
        'step time': 0.1
    }

    model = TrafficModel(param)
    result = model.run()

if __name__ == "__main__":
    main()