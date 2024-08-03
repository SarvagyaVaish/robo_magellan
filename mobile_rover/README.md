# Useful commands

## Development

### Run just the state machine

This is useful for testing the transition logic of the state machine. The robot's behaviors are noops.

```
python runner_robot_noop.py
```

### Run the state machine against a simulated robot

This is useful to test the logic of various robot behaviors. It uses a simulator robot.

TODO: Hook up a physics engine based simulator like WeBots. Replace the fake cone detections with images from the simulator's camera to test inference (sort of).

```
python runner_robot_sim.py
```

### Develop with live sensor data from the phone

1. Load DEV config in Sensor Log app
2. Run the following processes

```
python sensor_server.py
python pose_estimator.py
python runner_XYZ.py
```

### Replay logs

```
python data_publisher.py -d logs/run_1 -r 100
```

## Production

Running the developed behaviors on a real physical robot.

1. Load PROD config in Sensor Log app
2. Select PROD config in config_manager.py
3. Run the following processes

```
python sensor_server.py
python pose_estimator.py
python runner_magellan.py

python data_logger.py
```
