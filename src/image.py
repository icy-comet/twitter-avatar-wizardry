import math
from io import BytesIO
from typing import Tuple, Union, Optional
from PIL import Image, ImageDraw, ImageFont

# Base conf
h_w = 400  # square image
avatar_h_w = 360
base_size = (h_w, h_w)


def create_circular_mask(
    size: Tuple[float, float], angle: Optional[float] = 360
) -> Image.Image:
    """Create and return a circle/pieslice mask for any image.

    Args:
        size (Tuple[float, float]): A tuple containing image's (height, width).
        angle (Optional[float], optional): Pieslice's angle if necessary. Defaults to 360.

    Returns:
        Image.Image: The alpha-scheme mask image.
    """

    h, w = size
    mask_size = (h * 4, w * 4)
    alpha_image = Image.new("L", mask_size, 0)
    ImageDraw.Draw(alpha_image).pieslice(
        [(0, 0), mask_size], start=-90, end=angle - 90, fill=255
    )
    return alpha_image.resize(size=size, resample=Image.LANCZOS)


def create_slice(
    angle: float,
    txt: str,
    font_file: str,
    txt_color: str = "#ffffff",
    arc_clr: str = "#ffffff",
    gradient: Union[str, BytesIO] = None,
) -> Tuple[Image.Image, Image.Image]:
    """Create a new image with a pieslice and its mask.

    Args:
        angle (float): The angle the pieslice will cover out of 360.
        txt (str): Percent text to print on the slice.
        font_file (str): Path to the font's file to be used.
        txt_color (str, optional): Text's color. Defaults to "#ffffff".
        arc_clr (str, optional): Hex color to fill the slice with. Defaults to "#ffffff".
        gradient (Union[str, BytesIO], optional): Path/Bytes of the gradient image to be used. Defaults to None.

    Returns:
        Tuple[Image.Image, Image.Image]: A tuple containing the actual image as the first element and its maask as the second.
    """

    # other conf
    font = ImageFont.truetype(font_file, 10)
    upscaled_size = (h_w * 3, h_w * 3)

    # R = pieslice radius or half of the image dimensions - (10) visible ring's width
    # Calculated for base_size to avoid blurring text on resize
    # center_x & center_y aren't equal to R in a rectangle
    pieslice_radius = h_w // 2
    R = center_x = center_y = pieslice_radius - 10

    # -90 to start from top, -5 to offset text for readability
    txt_x = math.ceil(R * math.cos(math.radians(angle - 90 - 5)) + center_x)
    txt_y = math.ceil(R * math.sin(math.radians(angle - 90 - 5)) + center_y)

    if not gradient:
        progress_slice = Image.new(mode="RGBA", size=upscaled_size, color=(0, 0, 0, 0))
        ImageDraw.Draw(progress_slice).pieslice(
            ((0, 0), upscaled_size), start=-90, end=angle - 90, fill=arc_clr
        )
    else:
        progress_slice = Image.open(gradient).resize(upscaled_size, Image.LANCZOS)

    progress_slice = progress_slice.resize(base_size, Image.LANCZOS)
    ImageDraw.Draw(progress_slice).text((txt_x, txt_y), txt, fill=txt_color, font=font)
    progress_slice_mask = create_circular_mask(progress_slice.size, angle)

    return (progress_slice, progress_slice_mask)


def composite_avatar(
    og_avatar: Union[str, BytesIO],
    slice_img: Image.Image,
    slice_mask: Image.Image,
    gradient: Union[str, BytesIO] = None,
    base_clr: str = None,
) -> Image.Image:
    """Create a final composite avatar to be uploaded.

    Args:
        og_avatar (Union[str, BytesIO]): Path/Bytes of the untouched avatar.
        slice_img (Image.Image): The slice image to use in the composite.
        slice_mask (Image.Image): `slice_img`'s mask..
        gradient (Union[str, BytesIO], optional): Path/Bytes of the gradient image. Defaults to None.
        base_clr (str, optional): Hex color to fill the slice with. Defaults to None.

    Returns:
        Image.Image: A final composite avatar.
    """

    transparent_base = Image.new(mode="RGBA", size=base_size, color=(0, 0, 0, 0))
    og_avatar_size = (avatar_h_w, avatar_h_w)
    avatar = Image.open(og_avatar).convert("RGB").resize(og_avatar_size, Image.LANCZOS)

    if gradient:
        base_img = Image.open(gradient).resize(base_size, Image.LANCZOS)
    else:
        base_img = Image.new(mode="RGB", size=base_size, color=base_clr)

    bg_w, bg_h = base_img.size
    # avatar paste coordinates
    x = (bg_w - avatar_h_w) // 2  # center the avatar
    y = (bg_h - avatar_h_w) // 2

    base_img.paste(im=slice_img, box=(0, 0), mask=slice_mask)
    base_img.paste(im=avatar, box=(x, y), mask=create_circular_mask(avatar.size))
    transparent_base.paste(
        im=base_img, box=(0, 0), mask=create_circular_mask(base_img.size)
    )

    return transparent_base
