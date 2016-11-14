import basic_robot.robodemo as demo
from basic_robot.motors import Motors
from basic_robot.zumo_button import ZumoButton
from basic_robot.camera import Camera

c = Camera(img_height=40, img_width=60)
im = c.update()
im.convert("RGB")

r, g, b = 0, 0, 0
for i in range(c.img_width):
    for j in range(c.img_height):
        rn, gn, bn = im.getpixel((i, j))
        r += rn
        g += gn
        b += bn

total_pixels = c.img_height * c.img_width
r /= total_pixels
g /= total_pixels
b /= total_pixels

print(r, g, b)