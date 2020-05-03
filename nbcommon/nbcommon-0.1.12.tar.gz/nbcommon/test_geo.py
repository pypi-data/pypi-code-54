from . import geo
from .geo import GPSPin, cleanse

def test_parse_poly():
    thing = """who
cares
\t1.2\t3.4
\t5.6\t7.8
END 
END """
    r =  geo.parse_poly(thing)
    print(f'r is {r}')
    assert len(r) == 1
    assert r[0][0] == [1.2,3.4]


def test_parse_poly_file():
    with open('bangalore.poly') as f:
        p = geo.parse_poly(f.read())
        assert len(p) > 0


def test_cleanse():
    trajectory = open('trajectory.txt').read()
    raw= [GPSPin(lat=float(x),lng=float(y),ts=int(z)) for x,y,z in [item.split(',') for item in trajectory.split(';')]]
    pins = []
    last = None
    for pin in raw:
        if last:
            if pin.ts == last.ts:
                continue
        last = pin
        pins.append(pin) 

    r = cleanse(pins)
    assert len(r) != len(pins)
