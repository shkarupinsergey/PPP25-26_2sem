import math
import itertools
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from functools import reduce, wraps


def ploshad_poligona(pol):
    n = len(pol)
    s = 0
    for i in range(n):
        s += pol[i][0] * pol[(i + 1) % n][1] - pol[(i + 1) % n][0] * pol[i][1]
    return abs(s) / 2


def risuem_figuri(iter_poligonov, title="Рисунок"):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    kusok = list(itertools.islice(iter_poligonov, 25))

    for p_points in kusok:
        pol = patches.Polygon(p_points, closed=True, fill=True, alpha=0.5, edgecolor='black', facecolor='c')
        ax.add_patch(pol)

    ax.autoscale_view()
    plt.title(title)
    plt.grid(True, linestyle='--')
    plt.show()


def gen_rectangle(w=1, h=1, step=2):
    for n in itertools.count():
        x0 = n * step
        yield ((x0, 0), (x0, h), (x0 + w, h), (x0 + w, 0))


def gen_triangle(base=1, h=1, step=2):
    for n in itertools.count():
        x0 = n * step
        yield ((x0, 0), (x0 + base / 2, h), (x0 + base, 0))


def gen_hexagon(r=1, step=3):
    for n in itertools.count():
        cx = n * step
        tochki = []
        for i in range(6):
            ang = math.radians(60 * i)
            tochki.append((cx + r * math.cos(ang), r * math.sin(ang)))
        yield tuple(tochki)


def tr_translate(dx, dy):
    return lambda p: tuple((x + dx, y + dy) for x, y in p)


def tr_rotate(gradusi):
    rad = math.radians(gradusi)
    return lambda p: tuple(
        (x * math.cos(rad) - y * math.sin(rad), x * math.sin(rad) + y * math.cos(rad))
        for x, y in p
    )


def tr_symmetry(axis='x'):
    if axis == 'x':
        return lambda p: tuple((x, -y) for x, y in p)
    elif axis == 'y':
        return lambda p: tuple((-x, y) for x, y in p)
    return lambda p: tuple((-x, -y) for x, y in p)


def tr_homothety(k):
    return lambda p: tuple((x * k, y * k) for x, y in p)


def flt_convex_polygon():
    def check(pol):
        if len(pol) < 3: return False
        znaki = set()
        n = len(pol)
        for i in range(n):
            x1, y1 = pol[i]
            x2, y2 = pol[(i + 1) % n]
            x3, y3 = pol[(i + 2) % n]
            cross = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)
            if cross > 0:
                znaki.add(1)
            elif cross < 0:
                znaki.add(-1)
        return len(znaki) <= 1

    return check


def flt_angle_point(px, py):
    return lambda pol: any(abs(x - px) < 1e-5 and abs(y - py) < 1e-5 for x, y in pol)


def flt_square(max_s):
    return lambda pol: ploshad_poligona(pol) < max_s


def flt_short_side(max_len):
    def check(pol):
        n = len(pol)
        storoni = [math.hypot(pol[i][0] - pol[(i + 1) % n][0], pol[i][1] - pol[(i + 1) % n][1]) for i in range(n)]
        return min(storoni) < max_len

    return check


def flt_point_inside(px, py):
    def check(pol):
        n = len(pol)
        znaki = set()
        for i in range(n):
            x1, y1 = pol[i]
            x2, y2 = pol[(i + 1) % n]
            cross = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
            if cross > 0:
                znaki.add(1)
            elif cross < 0:
                znaki.add(-1)
        return len(znaki) <= 1

    return check


def flt_polygon_angles_inside(drugoy_pol):
    def check(pol):
        for px, py in drugoy_pol:
            if flt_point_inside(px, py)(pol):
                return True
        return False

    return check


def dec_tr_translate(dx, dy):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return map(tr_translate(dx, dy), func(*args, **kwargs))

        return wrapper

    return decorator


def agr_area(it):
    return reduce(lambda summ, p: summ + ploshad_poligona(p), it, 0)


def agr_min_area(it):
    return reduce(lambda m, p: min(m, ploshad_poligona(p)), it, float('inf'))


def agr_origin_nearest(it):
    dist = lambda p: min(math.hypot(x, y) for x, y in p)
    return reduce(lambda best, p: p if dist(p) < dist(best) else best, it)


def agr_max_side(it):
    def max_s(pol):
        n = len(pol)
        return max(math.hypot(pol[i][0] - pol[(i + 1) % n][0], pol[i][1] - pol[(i + 1) % n][1]) for i in range(n))

    return reduce(lambda m, p: max(m, max_s(p)), it, 0)


def agr_perimeter(it):
    def perim(pol):
        n = len(pol)
        return sum(math.hypot(pol[i][0] - pol[(i + 1) % n][0], pol[i][1] - pol[(i + 1) % n][1]) for i in range(n))

    return reduce(lambda summ, p: summ + perim(p), it, 0)


def zip_polygons(*iters):
    for t in zip(*iters):
        yield tuple(pt for pol in t for pt in pol)


def count_2D(start_x, start_y, step_x, step_y):
    n = 0
    while True:
        yield (start_x + n * step_x, start_y + n * step_y)
        n += 1


def zip_tuple(*iters):
    for items in zip(*iters):
        yield items


if __name__ == "__main__":
    mix = itertools.islice(itertools.chain(gen_rectangle(1, 1), gen_triangle(1, 1), gen_hexagon(0.6)), 7)
    risuem_figuri(mix, "Семь фигур")

    l1 = map(tr_rotate(30), gen_rectangle(1, 0.5, 2))
    l2 = map(tr_translate(0, 2), map(tr_rotate(30), gen_rectangle(1, 0.5, 2)))
    l3 = map(tr_translate(0, 4), map(tr_rotate(30), gen_rectangle(1, 0.5, 2)))
    risuem_figuri(itertools.chain(l1, l2, l3), "Три ленты под углом")

    krest1 = map(tr_translate(2, 5), map(tr_rotate(45), gen_rectangle(6, 1, 1)))
    krest2 = map(tr_translate(2, 5), map(tr_rotate(-45), gen_rectangle(6, 1, 1)))
    risuem_figuri(itertools.chain(krest1, krest2), "Пересекающиеся ленты")

    t1 = map(tr_translate(0, 1), gen_triangle(1, 1, 2))
    t2 = map(tr_symmetry('x'), map(tr_translate(0, -1), gen_triangle(1, 1, 2)))
    risuem_figuri(itertools.chain(t1, t2), "Симметричные треугольники")

    bazoviy_kvadrat = [((1, 0), (0, 1), (-1, 0), (0, -1))]
    scena_4_4 = (tr_homothety(k)(bazoviy_kvadrat[0]) for k in range(1, 10, 2))
    risuem_figuri(scena_4_4, "Масштаб между прямыми")

    kvadrati_15 = [tr_homothety(k)(((0, 0), (0, 1), (1, 1), (1, 0))) for k in range(1, 16)]
    korotkie = list(filter(flt_short_side(4), kvadrati_15))
    print(f"Осталось фигур после фильтра: {len(korotkie)}")
    print(f"Суммарная площадь оставшихся: {agr_area(korotkie)}")
