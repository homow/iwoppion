import taichi as ti
import handy_shader_functions as hsf

ti.init(arch=ti.cuda)

res_x = 512
res_y = 512
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))


@ti.kernel
def render(t: ti.f32):
    # draw something on your canvas
    for i, j in pixels:
        # init your canvas to black
        color = ti.Vector([i/res_x, j/res_y, ti.sin(t)/2+0.5])
        pixels[i, j] = color


gui = ti.GUI("Canvas", res=(res_x, res_y), fast_gui=True)

t = 0
while gui.running:
    t += 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()
