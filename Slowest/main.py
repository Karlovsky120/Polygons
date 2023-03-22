import json
import math
import numpy as np
import png
import time


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


def get_color(point, polygons):
    for polygon in polygons:
        if point.x < polygon.min_x or\
           point.x > polygon.max_x or\
           point.y < polygon.min_y or\
           point.y > polygon.max_y:
            continue

        polygon.points.append(polygon.points[0])

        total_angle = 0
        polygon_vertex_count = len(polygon.points)
        vectors_a = [0] * (2 * polygon_vertex_count)
        vectors_b = [0] * (2 * polygon_vertex_count)

        index = 0
        for first_vertex, second_vertex in zip(polygon.points, polygon.points[1:]):
            vectors_a[index] = first_vertex.y - point.y
            vectors_b[index] = first_vertex.x - point.x

            vectors_a[index + polygon_vertex_count] = second_vertex.y - point.y
            vectors_b[index + polygon_vertex_count] = second_vertex.x - point.x
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
            return 255

    return 0


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

        results = []
        pixels_processed = 0
        total_pixel_cunt = size_x * size_y
        for y in range(size_y):
            results.append([0] * size_x)
            for x in range(size_x):
                results[y][x] = get_color(Point(x + 0.5, y + 0.5), polygons)
            pixels_processed += size_x

            time_elapsed = time.perf_counter() - start_time
            ratio_done = pixels_processed / total_pixel_cunt
            print("Processed %.2f%% pixels in %.2f seconds. "
                  "Expected remaining runtime: %.2fs" % (100 * ratio_done,
                                                         time_elapsed,
                                                         time_elapsed / ratio_done - time_elapsed))

        print("Generated the image in %.5fs." % (time.perf_counter() - start_time))
        png.from_array(results, 'L').save('output.png')
        print("Generated and saved the image in %.5fs." % (time.perf_counter() - start_time))


if __name__ == '__main__':
    main_func()
