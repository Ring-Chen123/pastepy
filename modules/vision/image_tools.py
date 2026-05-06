"""
Name: Tiny Image Tools (no deps)

Why:
- Edge vision scripts sometimes need simple image operations without Pillow
- PPM/PGM are easy debug formats for raw camera frames

Features:
- PPM/PGM read/write
- grayscale conversion
- crop, resize, tile
- frame sampling and manifests

Limitations:
- P3/P2 ASCII formats only
- Nearest-neighbor resize only
"""

import json
import os


def image_dimensions(image):
    return image["width"], image["height"]


def read_ppm(path):
    with open(path, "r", encoding="ascii") as f:
        tokens = f.read().split()
    if tokens[0] != "P3":
        raise ValueError("expected P3 PPM")
    width, height = int(tokens[1]), int(tokens[2])
    values = [int(v) for v in tokens[4:]]
    pixels = [tuple(values[i:i + 3]) for i in range(0, len(values), 3)]
    return {"mode": "RGB", "width": width, "height": height, "pixels": pixels}


def write_ppm(path, image):
    with open(path, "w", encoding="ascii") as f:
        f.write("P3\n%d %d\n255\n" % (image["width"], image["height"]))
        for r, g, b in image["pixels"]:
            f.write("%d %d %d\n" % (r, g, b))


def read_pgm(path):
    with open(path, "r", encoding="ascii") as f:
        tokens = f.read().split()
    if tokens[0] != "P2":
        raise ValueError("expected P2 PGM")
    width, height = int(tokens[1]), int(tokens[2])
    return {"mode": "L", "width": width, "height": height, "pixels": [int(v) for v in tokens[4:]]}


def write_pgm(path, image):
    with open(path, "w", encoding="ascii") as f:
        f.write("P2\n%d %d\n255\n" % (image["width"], image["height"]))
        for value in image["pixels"]:
            f.write("%d\n" % value)


def rgb_to_grayscale(image):
    pixels = [int(0.299 * r + 0.587 * g + 0.114 * b) for r, g, b in image["pixels"]]
    return {"mode": "L", "width": image["width"], "height": image["height"], "pixels": pixels}


def crop(image, x, y, width, height):
    pixels = []
    for row in range(y, y + height):
        start = row * image["width"] + x
        pixels.extend(image["pixels"][start:start + width])
    return {"mode": image["mode"], "width": width, "height": height, "pixels": pixels}


def resize_nearest(image, width, height):
    pixels = []
    for y in range(height):
        src_y = int(y * image["height"] / height)
        for x in range(width):
            src_x = int(x * image["width"] / width)
            pixels.append(image["pixels"][src_y * image["width"] + src_x])
    return {"mode": image["mode"], "width": width, "height": height, "pixels": pixels}


def tile_image(image, tile_width, tile_height):
    tiles = []
    for y in range(0, image["height"], tile_height):
        for x in range(0, image["width"], tile_width):
            tiles.append(crop(image, x, y, min(tile_width, image["width"] - x), min(tile_height, image["height"] - y)))
    return tiles


def frame_schedule(total_frames, every=1, limit=None):
    frames = list(range(0, total_frames, every))
    return frames[:limit] if limit is not None else frames


def write_frame_manifest(path, frames):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(frames, f, indent=2, sort_keys=True)
        f.write("\n")


def clamp_box(box, width, height):
    x1, y1, x2, y2 = box
    return [max(0, x1), max(0, y1), min(width, x2), min(height, y2)]


def box_center(box):
    return ((box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0)


def xywh_to_xyxy(box):
    x, y, w, h = box
    return [x, y, x + w, y + h]


def xyxy_to_xywh(box):
    x1, y1, x2, y2 = box
    return [x1, y1, x2 - x1, y2 - y1]


if __name__ == "__main__":
    print("[TEST] image_tools")
    try:
        img = {"mode": "RGB", "width": 2, "height": 1, "pixels": [(255, 0, 0), (0, 0, 255)]}
        assert image_dimensions(img) == (2, 1)
        assert rgb_to_grayscale(img)["pixels"][0] == 76
        assert crop(img, 1, 0, 1, 1)["pixels"] == [(0, 0, 255)]
        assert resize_nearest(img, 1, 1)["width"] == 1
        assert len(tile_image(img, 1, 1)) == 2
        assert frame_schedule(5, every=2) == [0, 2, 4]
        assert clamp_box([-1, -1, 3, 3], 2, 2) == [0, 0, 2, 2]
        assert box_center([0, 0, 2, 2]) == (1, 1)
        assert xywh_to_xyxy([1, 2, 3, 4]) == [1, 2, 4, 6]
        assert xyxy_to_xywh([1, 2, 4, 6]) == [1, 2, 3, 4]
        print("[OK] image helpers")
        print("[DONE]")
    except Exception as e:
        print("[FAIL]", e)
