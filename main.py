# A Cropper - Image cropping script
# Dr Lee A. Christie
# GitHub: @leechristie
# Mastodon: @0x1ac@techhub.social
# Sunday, 6th October 2024


from PIL import Image
from tqdm.auto import tqdm
import os


INPUT_FOLDER: str = './input'
OUTPUT_FOLDER: str = './output'


# SET CROP PARAMETERS HERE - BEFORE SPLIT
LEFT_CROP = 390
RIGHT_CROP = 388
TOP_CROP = 0
BOTTOM_CROP = 0

# SET SPLIT PARAMETERS HERE
SPLIT_LEFT_RIGHT = True
REVERSE_SIDE_ORDER = False

# SET SECOND CROP PARAMETERS HERE - AFTER SPLIT
SECOND_UNIFORM_CROP = 4


def crop(image: Image, left: int, right: int, top: int, bottom: int) -> Image:
    width, height = image.size
    new_width = width - left - right
    new_height = height - top - bottom
    assert (new_width > 0 and new_height > 0), f'cropped image has zero area; check crop parameters'
    return image.crop((left, top, width - right, height - bottom))


def left_right_split(image: Image) -> tuple[Image, Image]:
    width, height = image.size
    assert (width % 2 == 0), f'cropped image has odd width; check crop parameters'
    half = width // 2
    left, right = image.crop((0, 0, half, height)), image.crop((half, 0, width, height))
    if REVERSE_SIDE_ORDER:
        return right, left
    return left, right


def main() -> None:

    input_files: list[str] = sorted(map(lambda f: os.path.join(INPUT_FOLDER, f),
                                    filter(lambda f: f.endswith('.png'),
                                           os.listdir(INPUT_FOLDER))))

    index = 0
    for input_file in tqdm(input_files):

        with Image.open(input_file) as image:
            images: tuple[Image, ...] = (crop(image, LEFT_CROP, RIGHT_CROP, TOP_CROP, BOTTOM_CROP), )

        if SPLIT_LEFT_RIGHT:
            image, = images
            images = left_right_split(image)

        for image in images:
            image = crop(image, SECOND_UNIFORM_CROP, SECOND_UNIFORM_CROP, SECOND_UNIFORM_CROP, SECOND_UNIFORM_CROP)
            outfile = os.path.join(OUTPUT_FOLDER, f'{index:08}.png')
            assert (not os.path.exists(outfile)), f'{outfile} already exits; clear output directory'
            image.save(outfile)
            index += 1


if __name__ == '__main__':
    main()
