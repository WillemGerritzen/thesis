from PIL import Image, ImageDraw


def test_pil() -> None:
    im = Image.new("RGB", (150, 100), (255, 255, 255))

    # draw = ImageDraw.Draw(im)
    # draw.line((0, 0) + im.size, fill=128)
    # draw.line((0, im.size[1], im.size[0], 0), fill=128)

    # write to stdout
    im.save("C:\\Users\Willem\Documents\Github\\thesis\images", "PNG")
