import base64
from io import BytesIO
from typing import Tuple
from twitter import User
from config import Config
from image import create_slice, composite_avatar


def calculate_progress(followers: int, track_mark: int) -> Tuple[int, float]:
    # followers % track_mark helps calulate progress for every lapse of desired followers
    percentage = ((followers % track_mark) / track_mark) * 100
    angle = (percentage / 100) * 360
    return (int(percentage), float(angle))


def update_cached_avatar(user: User, cache: dict) -> dict:
    """Download `og_avatar` off Twitter and cache it.

    Args:
        user (User): User Object.
        cache (dict): A dictionary of cached data.

    Returns:
        dict: Updated cache dictionary.
    """
    og_avatar = user.fetch_avatar()
    og_avatar_bytes = BytesIO()
    og_avatar.save(og_avatar_bytes, "JPEG")
    og_avatar = base64.b64encode(og_avatar_bytes.getvalue()).decode("utf-8")
    cache.update({"og_avatar": og_avatar})
    return cache


def update_progress(
    user: User, cache: dict, percent_progress: int, slice_angle: float
) -> dict:
    """Update Twitter's avatar with the (new) progress.

    Args:
        user (User): User object.
        cache (dict): A dictionary containing cached data.
        percent_progress (int): Current progress in percentage.
        slice_angle (float): [description]

    Returns:
        dict: [description]
    """

    og_avatar_buffer = BytesIO(base64.b64decode(cache["og_avatar"].encode("utf-8")))

    if Config.use_gradient:
        slice_img, slice_mask = create_slice(
            angle=slice_angle,
            txt=str(percent_progress) + "%",
            txt_color=Config.txt_color,
            font_file=Config.font_file,
            gradient=Config.arc_gradient,
        )

        composite_img = composite_avatar(
            og_avatar=og_avatar_buffer,
            slice_img=slice_img,
            slice_mask=slice_mask,
            gradient=Config.base_gradient,
        )
    else:
        slice_img, slice_mask = create_slice(
            angle=slice_angle,
            txt=str(percent_progress) + "%",
            txt_color=Config.txt_color,
            font_file=Config.font_file,
            arc_clr=Config.arc_solid_clr,
        )

        composite_img = composite_avatar(
            og_avatar=og_avatar_buffer,
            slice_img=slice_img,
            slice_mask=slice_mask,
            base_clr=Config.base_solid_clr,
        )

    new_avatar = BytesIO()
    composite_img.save(new_avatar, "PNG")
    avatar_url = user.update_avatar(new_avatar)
    cache.update({"percent_progress": percent_progress, "avatar_url": avatar_url})
    return cache
