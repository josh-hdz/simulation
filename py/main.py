from traffic_model import TrafficModel

def main():
    param = {
        "car": {
            "amount": 20,
            "length range": (2.5, 4.5),
            "max vel range": (1.0, 2.0),
            "min dist range": (3.0, 5.0)
        },
        'traffic lights': {
            'amount': 4,
            'time red': 2,
            'time yellow': 1,
            'time green': 2
        },
        'a': 400,
        'step time': 0.01,
        'b': 5,
        'l': 3.6,
        'density': [0.25, 0.3, 0.4, 0.05],
        'steps': 10000 
    }

    model = TrafficModel(param)
    result = model.run()

if __name__ == "__main__":
    main()