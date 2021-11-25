from traffic_model import TrafficModel

def main():
    param = {
        "car": {
            "amount": 8,
            "length range": (2.5, 4.5),
            "max vel range": (1.0, 2.0),
            "min dist range": (3.0, 5.0)
        },
        'traffic lights': {
            'amount': 2,
            'time red': 45,
            'time yellow': 5,
            'time green': 50
        },
<<<<<<< HEAD
        'a': 400,
        'step time': 0.01,
=======
        'a': 500,
        'step time': 0.1,
>>>>>>> fabe1700162b8c9992747726300458f36d19eb8c
        'b': 5,
        'l': 3.6,
        "density": 0.5,
        'steps': 10000,
        
    }

    model = TrafficModel(param)
    result = model.run()

if __name__ == "__main__":
    main()