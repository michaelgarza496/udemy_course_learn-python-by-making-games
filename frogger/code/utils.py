from pygame.sprite import Group
from pygame.image import load
from pygame import Surface
from pathlib import Path

BASE_PATH = Path("frogger/graphics")


def create_group(all_groups: list, add_to_all_groups: bool = True) -> Group:
    g: Group = Group()
    if add_to_all_groups:
        all_groups.append(g)
    return g


def load_image(
    file_path: str, file_name: str, convert_alpha: bool = True, format: str = "png"
) -> Surface:
    img_path = Path(BASE_PATH / file_path / (file_name + "." + format))
    return load(img_path).convert_alpha() if convert_alpha else load(img_path).convert()


def load_images(
    files_path: str, in_range: int = 0, convert_alpha: bool = True, format: str = "png"
) -> list:
    images = []
    if in_range:
        for i in range(in_range + 1):
            image = load_image(
                files_path, str(i), convert_alpha=convert_alpha, format=format
            )
            images.append(image)
    return images
