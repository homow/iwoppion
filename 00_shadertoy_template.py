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
        # Trans the short side to [-1, 1]
        u = ti.cast(i, ti.f32)/res_x*2 - 1.0
        v = ti.cast(j, ti.f32)/res_y*2 - 1.0
        if res_x > res_y:
            u *= res_x / res_y
        else:
            v *= res_y / res_x
        # init your canvas to black
        color = ti.Vector([ti.abs(u), ti.abs(v), ti.sin(t)*2 - 1.0])
        pixels[i, j] = color


gui = ti.GUI("Canvas", res=(res_x, res_y), fast_gui=True)

t = 0
while gui.running:
    t += 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()
