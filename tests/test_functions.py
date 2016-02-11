from app.main.anneal import euclidean_distance, neighbor, cost, Point


def almost_equals(a, b, precision=4):
    return round(abs(a - b), precision) == 0.

def test_distance():
    a, b = Point('a', 3, 0), Point('b', 0, 4)
    assert almost_equals(euclidean_distance(a, b), 5)
    c, d = Point('c', 5, 0), Point('d', 0, 12)
    assert almost_equals(euclidean_distance(c, d), 13)

def test_cost():
    a, b = Point('a', 3, 0), Point('b', 0, 4)
    assert almost_equals(cost([a, b]), 10)

def test_neighbor():
    s = range(20)
    n = neighbor(s)
    counts = 0
    for i, j in zip(s, n):
        if i != j:
            counts += 1
    assert counts == 2
