from pygame.sprite import Group
from pygame.image import load
from pygame import Surface
from random import choice
import os

BASE_PATH = "frogger"


def create_group(all_groups: list, add_to_all_groups: bool = True) -> Group:
    g: Group = Group()
    if add_to_all_groups:
        all_groups.append(g)
    return g


def load_image(file_path: str, convert_alpha: bool = True) -> Surface:
    file_path = f"{BASE_PATH}/{file_path.lstrip(BASE_PATH)}"
    return (
        load(file_path).convert_alpha() if convert_alpha else load(file_path).convert()
    )


# def load_image(file_path: str, convert_alpha: bool = True) -> Surface:
#     file_path = file_path.removeprefix(str(BASE_PATH) + '/')
#     img_path = Path(BASE_PATH / file_path)
#     return load(img_path).convert_alpha() if convert_alpha else load(img_path).convert()


def load_images_animation(files_path: str, convert_alpha: bool = True) -> dict:
    images = {}
    files_path = f"{BASE_PATH}/{files_path}"
    for index, content in enumerate(os.walk(files_path)):
        if index == 0:
            continue
        root, _, files = content
        root = root.replace("\\", "/")
        key = root.split("/")[-1]
        images[key] = [
            load_image(f"{root}/{img}", convert_alpha=convert_alpha)
            for img in sorted(files)
        ]
    return images


def load_images_list(files_path: str, convert_alpha: bool = True) -> list:
    images = []
    files_path = f"{BASE_PATH}/{files_path}"
    for root, _, files in os.walk(files_path):
        if files:
            for file in files:
                root = root.replace("\\", "/")
                images.append(load_image(f"{root}/{file}", convert_alpha=convert_alpha))
    return images


def get_random_image(files_path: str, convert_alpha: bool = True) -> Surface:
    return choice(load_images_list(files_path, convert_alpha=convert_alpha))


#     files = sorted(str(file) for file in Path(BASE_PATH / files_path).iterdir() if file.is_file())
#     # images = [load_image(file, convert_alpha=convert_alpha) for file in files]
#     return images

# def load_images(files_path: str, convert_alpha: bool = True) -> list:
#     files = sorted(str(file) for file in Path(BASE_PATH / files_path).iterdir() if file.is_file())
#     images = [load_image(file, convert_alpha=convert_alpha) for file in files]
#     return images

# def load_image(
#     file_path: str, file_name: str, convert_alpha: bool = True, format: str = "png"
# ) -> Surface:
#     img_path = Path(BASE_PATH / file_path / (file_name + "." + format))
#     return load(img_path).convert_alpha() if convert_alpha else load(img_path).convert()

# def load_images(
#     files_path: str, in_range: int = 0, convert_alpha: bool = True, format: str = "png"
# ) -> list:
#     images = []
#     if in_range:
#         for i in range(in_range + 1):
#             image = load_image(
#                 files_path, str(i), convert_alpha=convert_alpha, format=format
#             )
#             images.append(image)
#     return images
