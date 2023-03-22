import json
import png
import time

from shapely import Point, Polygon, MultiPolygon


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

        result = []
        for y in range(0, size_y):
            result.append([0] * size_x)
            for x in range(0, size_x):
                result[y][x] = 255 if multipolygon.contains(Point(x + 0.5, y + 0.5)) else 0

        print("Generated the image in %.5fs." % (time.perf_counter() - start_time))
        png.from_array(result, 'L').save('output.png')
        print("Generated and saved the image in %.5fs." % (time.perf_counter() - start_time))


if __name__ == '__main__':
    main_func()
