import math
from io import BytesIO
from typing import Tuple, Union, Optional
from PIL import Image, ImageDraw, ImageFont

# Base conf
h_w = 400 # square image
base_size = (h_w, h_w)

def calculate_progress(followers: int, track_mark: int) -> Tuple[int, float]:
    # followers % track_mark helps calulate progress for every lapse of desired followers
    percentage = ((followers%track_mark)/track_mark)*100
    angle = (percentage/100)*360
    print('completed calculations')
    return (int(percentage), float(angle))

def create_circular_mask(size: Tuple[float, float], angle: Optional[float] = 360) -> Image.Image:
    """Return a circular/sliced alpha-mask image.

    Parameters
    ----------
    size : Tuple[float, float]
        A tuple with (height, width) of the image to be masked.
    ell_end : float, optional
        Angle to be covered by pieslice, by default 360 (full circle)

    Returns
    -------
    Image.Image
        Alpha mask.
    """

    h, w = size
    mask_size = (h*4, w*4)
    alpha_image = Image.new('L', mask_size, 0)
    ImageDraw.Draw(alpha_image).pieslice([(0, 0), mask_size], start=-90, end=angle-90, fill=255)
    return alpha_image.resize(size=size, resample=Image.LANCZOS)

def create_slice(angle: float,
                 txt: str,
                 font_file: str,
                 txt_color: str = "#000000",
                 arc_clr: str = "#ffffff",
                 gradient: Union[str, BytesIO] = None) -> Image.Image:
    """Return a new image with a slice with passed specs.

    Parameters
    ----------
    angle : float
        Angle the pieslice occupies out of 360.
    txt : str
        Text string to print on slice.
    font_file : str
        Path to the font file in use.
    txt_color : str, optional
        Text color on the ring, by default "#000000"
    arc_clr : str, optional
        Hex color to fill the slice with, by default "#ffffff"
    gradient : Union[str, BytesIO], optional
        Gradient file's bytes/path to be used, by default None

    Returns
    -------
    Image.Image
        An Image with a slice on it.
    """

    # other conf
    font = ImageFont.truetype(font_file, 30)
    upscaled_size = (h_w*3, h_w*3)
    pieslice_radius = (h_w*3)//2

    # R = Pieslice Radius/half of the image dimensions - 40 visible ring's width + 2 offset
    # center_x & center_y don't equal R in a rectangle
    R = center_x = center_y = pieslice_radius - 40 + 2

    # -90 to start from top,-5 to offset text for readability
    # +5 to offset final co-ordinates for readability
    txt_x = math.ceil(R * math.cos(math.radians(angle - 90 - 5)) + center_x + 5)
    txt_y = math.ceil(R * math.sin(math.radians(angle - 90 - 5)) + center_y + 5)

    if not gradient:
        progress_slice = Image.new(mode="RGBA", size=upscaled_size, color=(0, 0, 0, 0))
        progress_slice_drawing = ImageDraw.Draw(progress_slice)
        progress_slice_drawing.pieslice(((0,0), upscaled_size), start=-90, end=angle-90, fill=arc_clr)
    else:
        progress_slice = Image.open(gradient).resize(upscaled_size, Image.LANCZOS)
        progress_slice_drawing = ImageDraw.Draw(progress_slice)

    progress_slice_drawing.text((txt_x, txt_y), txt, fill=txt_color, font=font)
    progress_slice = progress_slice.resize(base_size, Image.LANCZOS)

    return progress_slice

def composite_avatar(og_avatar: Union[str, BytesIO],
                     slice_img: Image.Image,
                     slice_angle: float,
                     gradient: Union[str, BytesIO] = None,
                     base_clr: str = None) -> Image.Image:
    """Return a final transparent composite image.

    Parameters
    ----------
    og_avatar : Union[str, BytesIO]
        Untouched avatar's path/bytes.
    slice_img : Image.Image
        Slice image to paste.
    slice_angle : float
        Slice angle in the `slice_img` to create mask.
    gradient : Union[str, BytesIO], optional
        Gradient file's path/bytes, by default None
    base_clr : str, optional
        Hex color to fill the base image, by default None

    Returns
    -------
    Image.Image
        A final transparent composite image.
    """

    transparent_base = Image.new(mode="RGBA", size=base_size, color=(0,0,0,0))
    og_avatar_size = (350, 350)
    avatar = Image.open(og_avatar).convert("RGB").resize(og_avatar_size, Image.LANCZOS)

    if gradient:
        base_img = Image.open(gradient).resize(base_size, Image.LANCZOS)
    else:
        base_img = Image.new(mode="RGB", size=base_size, color=base_clr)

    bg_w, bg_h = base_img.size
    # avatar paste coordinates
    x = (bg_w-350)//2 # center the avatar
    y = (bg_h-350)//2

    base_img.paste(im=slice_img, box=(0, 0), mask=create_circular_mask(slice_img.size, slice_angle))
    base_img.paste(im=avatar, box=(x,y), mask=create_circular_mask(avatar.size))
    transparent_base.paste(im=base_img, box=(0, 0), mask=create_circular_mask(base_img.size))

    return transparent_base
