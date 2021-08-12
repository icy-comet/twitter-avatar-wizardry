import base64
from os import getenv
from io import BytesIO
from typing import Any
from twitter import User
from config import Config
from image import create_slice, create_composite, calculate_progress
from deta import app, Deta

deta = Deta(getenv("DETA_PROJECT_KEY"))
db = deta.Base("random")
db_key = "twitter-progress-bar"

@app.lib.cron()
def cron_job(event: Any):
    """Run at set intervals and update image and cache as required.

    Parameters
    ----------
    event : Any
        An object passed by Deta that includes the event's payload (if any) and its type.
    """
    user = User()
    cache: dict = db.get(db_key)
    percent_progress, slice_angle = calculate_progress(user.followers_count, Config.track_mark)

    if not user.profile_img_url == cache["avatar_url"]:
        og_avatar = user.fetch_avatar()
        og_avatar_bytes = BytesIO()
        og_avatar.save(og_avatar_bytes, "JPEG")
        og_avatar = base64.b64encode(og_avatar_bytes.getvalue()).decode("utf-8")
        cache.update({'og_avatar': og_avatar})

    if not percent_progress == cache["percent_progress"]:
        
        base_img_buffer = BytesIO(base64.b64decode(cache["og_avatar"].encode("utf-8")))

        if Config.use_gradient:
            slice_img = create_slice(slice_angle, str(percent_progress)+"%", Config.txt_color, gradient=Config.arc_gradient)
            composite_img = create_composite(base_img_buffer, slice_img, slice_angle, gradient=Config.base_gradient)
        else:
            slice_img = create_slice(slice_angle, str(percent_progress)+"%", Config.txt_color, slice_color=Config.arc_solid_clr)
            composite_img = create_composite(base_img_buffer, slice_img, slice_angle, base_fill_clr=Config.base_solid_clr)

        new_avatar = BytesIO()
        composite_img.save(new_avatar, "PNG")
        avatar_url = user.update_avatar(new_avatar)
        cache.update({"percent_progress": percent_progress, "avatar_url": avatar_url})

    db.put(cache, db_key)

@app.lib.run(action="reset-count")
def run_now(event):
    """ Manipulate cached progress to force update on next CRON. """
    db.update({"percent_progress": 0}, db_key)
    return "Count Reset"

@app.lib.run(action="full-reset")
def full_reset(event):
    """ Empty the entire cache. """
    db.put({"percent_progress": 0, "og_avatar": "", "avatar_url": ""})
