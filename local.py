from image import create_slice, composite_avatar
from config import Config

angle = 234
txt = "65%"
og_avatar = "raw_avatar.png"

slice_img, slice_mask = create_slice(angle,
                                    txt,
                                    txt_color=Config.txt_color,
                                    font_file=Config.font_file,
                                    gradient=Config.arc_gradient)

composite_img = composite_avatar(og_avatar,
                                slice_img=slice_img,
                                slice_mask=slice_mask,
                                gradient=Config.base_gradient)

composite_img.save("processed_avatar.png", "PNG")