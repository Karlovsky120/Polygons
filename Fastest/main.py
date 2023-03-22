import json
import time

from PIL import Image, ImageDraw


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
                points.append((point['x'] * size_x, (1 - point['y']) * size_y))
            polygons.append(points)

        image = Image.new("L", (size_x, size_y))
        draw = ImageDraw.Draw(image)
        for polygon in polygons:
            draw.polygon(polygon, fill="white")

        print("Generated the image in %.5fs." % (time.perf_counter() - start_time))
        image.save("output.png")
        print("Generated and saved the image in %.5fs." % (time.perf_counter() - start_time))


if __name__ == '__main__':
    main_func()
