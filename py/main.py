from traffic_model import TrafficModel

def main():
    param = {
        "car": {
            "amount": 100,
            "length range": (1.8, 2.3),
            "max vel range": (10.0, 16.67),
            "min dist range": (0.5, 1.0)
        },
        'a': 1000,
        'step time': 0.1,
        'b': 5,
        'l': 3.6,
        "density": 0.5
    }

    model = TrafficModel(param)
    result = model.run()
    print(result)
if __name__ == "__main__":
    main()