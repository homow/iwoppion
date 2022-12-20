# plot math functions
# canvas mapped to [-1, 1]

import taichi as ti
import handy_shader_functions as hsf

ti.init(arch=ti.cuda)

res_x = 512
res_y = 512
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))


@ti.func
def plot(a: ti.f32, b: ti.f32):
    return hsf.smoothstep(0.02, 0, ti.abs(a-b))


@ti.kernel
def render(t: ti.f32):
    # draw something on your canvas
    for i, j in pixels:
        x = (ti.cast(i, ti.f32)/res_x - 0.5) * 2
        # y = 8*(ti.sin(x/8))+res_y/2
        y = x
        y_j = (ti.cast(j, ti.f32)/res_y - 0.5) * 2
        pct = plot(y, y_j)
        color = ti.Vector([0.0, 0.0, 0.0])
        color += pct*ti.Vector([0.0, 1.0, 0.0])
        pixels[i, j] = color


gui = ti.GUI("Canvas", res=(res_x, res_y), fast_gui=True)

t = 0
while gui.running:
    t += 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()
