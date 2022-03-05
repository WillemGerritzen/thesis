from PIL import Image, ImageDraw


def generate_empty_canvas() -> None:
    """ Generate a white canvas of 240 by 180 pixels in bitmap format """
    canvas = Image.new("RGB", (240, 180), (255, 255, 255))  # 240x180 pixels white canvas

    canvas.save("images/test", format="bmp")  # Save in images directory in bitmap format


def draw_polygon() -> None:
    with Image.open("images/test") as im:
        draw = ImageDraw.Draw(im)
        draw.polygon(((0, 0), (10, 0), (0, 10)), fill=128)
        print((0, 0) + im.size)
        # draw.line((randint(0, im.size[0]), randint(0, im.size[1])), fill=64)

        im.save("images/test2", "bmp")
