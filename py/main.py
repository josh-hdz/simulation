from traffic_model import TrafficModel

def main():
    param = {
        "car": {
<<<<<<< HEAD
            "amount": 10,
            "length range": (2.5, 4.5),
=======
            "amount": 20,
            "length range": (20, 30),
>>>>>>> 85a4236ac7bbec9edd6b35eee82f7036d563dfce
            "max vel range": (1.0, 2.0),
            "min dist range": (20.0, 30.0)
        },
        'traffic lights': {
            'amount': 4,
            'time yellow': 0.5,
            'time green': 1
        },
<<<<<<< HEAD
        'a': 200,
        'b': 5,
        'l': 3.6,
        'steps': 1000, 
        'step time': 0.01,
        'density': (0.20, 0.42, 0.23, 0.15),
        'dead time': 0.3
=======
        'a': 1000,
        'step time': 0.01,
        'b': 30,
        'l': 30,
        'density': (0.20, 0.42, 0.23, 0.15),
        'steps': 20000
>>>>>>> 85a4236ac7bbec9edd6b35eee82f7036d563dfce
    }

    model = TrafficModel(param)
    result = model.run()

if __name__ == "__main__":
    main()
