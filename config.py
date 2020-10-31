class ImageConverterConfig:
    def __init__(self, img_width: int = 120):
        self.img_width = img_width


class ProgramConfiguration:
    def __init__(self, check_interval: int, tag: str, messages_to_take: int, display_image: bool):
        self.check_interval: int = check_interval
        self.tag: str = tag
        self.messages_to_take: int = messages_to_take
        self.display_image: bool = display_image
