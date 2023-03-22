import json
import multiprocessing
import png
import time

from multiprocessing import Pool
from shapely import Point, Polygon, MultiPolygon


def get_color(multipolygon, point):
    return point, 255 if multipolygon.contains(Point(point[0] + 0.5, point[1] + 0.5)) else 0


def main_func():
    start_time = time.perf_counter()
    with open("..\\input.json", 'rb') as file:
        input_json = json.load(file)

        size_x = input_json['size']['x']
        size_y = input_json['size']['y']

        polygons = []
        for region in input_json['regions']:
            polygon_points = []
            for point in region['positions']:
                polygon_points.append((point['x'] * size_x, (1 - point['y']) * size_y))
            polygons.append(Polygon(polygon_points))
        multipolygon = MultiPolygon(polygons)

        points = []
        results = []

        thread_pool = Pool(processes=multiprocessing.cpu_count())
        for y in range(size_y):
            results.append([0] * size_x)
            for x in range(size_x):
                points.append((x, y))

        for (x_out, y_out), result in thread_pool.starmap(get_color,
                                                          [(multipolygon, point) for point in points],
                                                          chunksize=100 * multiprocessing.cpu_count()):
            results[y_out][x_out] = result

        print("Generated the image in %.5fs." % (time.perf_counter() - start_time))
        png.from_array(results, 'L').save('output.png')
        print("Generated and saved the image in %.5fs." % (time.perf_counter() - start_time))


if __name__ == '__main__':
    main_func()
