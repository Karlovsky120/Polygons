import json
import math
import multiprocessing
import numpy as np
import png
import time

from multiprocessing import Pool


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Polygon:
    def __init__(self, points, min_x, max_x, min_y, max_y):
        self.points = points
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y


def get_color(pixel, polygons):
    pixel_center = Point(pixel.x + 0.5, pixel.y + 0.5)

    for polygon in polygons:
        if pixel_center.x < polygon.min_x or \
           pixel_center.x > polygon.max_x or \
           pixel_center.y < polygon.min_y or \
           pixel_center.y > polygon.max_y:
            continue

        polygon.points.append(polygon.points[0])

        total_angle = 0
        polygon_vertex_count = len(polygon.points)
        vectors_a = [0] * (2 * polygon_vertex_count)
        vectors_b = [0] * (2 * polygon_vertex_count)

        index = 0
        for first_vertex, second_vertex in zip(polygon.points, polygon.points[1:]):
            vectors_a[index] = first_vertex.y - pixel_center.y
            vectors_b[index] = first_vertex.x - pixel_center.x

            vectors_a[index + polygon_vertex_count] = second_vertex.y - pixel_center.y
            vectors_b[index + polygon_vertex_count] = second_vertex.x - pixel_center.x
            index += 1

        angles = np.arctan2(vectors_a, vectors_b)

        for positive, negative in zip(angles[:polygon_vertex_count], angles[polygon_vertex_count:]):
            angle = positive - negative

            while angle > math.pi:
                angle -= math.tau
            while angle < -math.pi:
                angle += math.tau

            total_angle += angle

        if math.fabs(total_angle) > math.pi:
            return pixel, 255

    return pixel, 0


def main_func():
    start_time = time.perf_counter()
    with open("..\\input.json", 'rb') as file:
        input_json = json.load(file)

        size_x = input_json['size']['x']
        size_y = input_json['size']['y']

        polygons = []
        for region in input_json['regions']:
            points = []
            for point in region['positions']:
                points.append(Point(point['x'] * size_x, (1 - point['y']) * size_y))
            all_x = [point.x for point in points]
            all_y = [point.y for point in points]
            polygons.append(Polygon(points, min(all_x), max(all_x), min(all_y), max(all_y)))

        points = []
        results = []

        thread_pool = Pool(processes=multiprocessing.cpu_count())
        for y in range(size_y):
            results.append([0] * size_x)
            for x in range(size_x):
                points.append(Point(x, y))

        for pixel, result in thread_pool.starmap(get_color,
                                                 [(point, polygons) for point in points],
                                                 chunksize=100 * multiprocessing.cpu_count()):
            results[pixel.y][pixel.x] = result

        print("Generated the image in %.5fs." % (time.perf_counter() - start_time))
        png.from_array(results, 'L').save('output.png')
        print("Generated and saved the image in %.5fs." % (time.perf_counter() - start_time))


if __name__ == '__main__':
    main_func()
