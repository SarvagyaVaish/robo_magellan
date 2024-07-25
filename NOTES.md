## Apr 29, 2024

Create a pyenv virtualenv named robomagellan:

```
pyenv install 3.10.12
pyenv virtualenv 3.10.12 robomagellan
pyenv local robomagellan
pip install -r requirements.txt
```

Terminology

GPS

- latitude: gps coordinate
- longitude: gps coordinate
- heading:
  - radians `[0, 2pi)`
  - 0 deg = north
  - left-hand rule rotation
  - to convert to right handed cartesian
    = `-1 * heading  +  pi / 2`
