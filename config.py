class Config:
    """App configuration"""

    track_mark: int = 100  # reset ring for every 100 followers
    txt_color: str = "#000000"  # hex color of the percent txt

    use_gradient: bool = True  # use gradient images

    # paths to images (relative to working dir)
    base_gradient: str = "base_gradient.png"
    arc_gradient: str = "arc_gradient.png"

    # hex colors if `use_gradient` is set to false
    base_clr: str = "#000000"
    arc_clr: str = "#ffffff"

    font_file: str = "poppins_regular.ttf"  # path to a font-file
