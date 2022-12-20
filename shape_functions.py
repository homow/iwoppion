import taichi as ti
import handy_shader_functions as hsf

ti.init(arch=ti.cuda)

res_x = 512
res_y = 512
pixels = ti.Vector.field(3, ti.f32, shape=(res_x, res_y))


@ti.func
def rect():
    pass


@ti.func
def line(a: ti.f32, b: ti.f32, u: ti.f32, v: ti.f32):
    # todo: exchange 1 and 0
    return 0.0 if (hsf.step(a, u) - hsf.step(b, u) == 1.0) else 1.0


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
        left = hsf.step(-0.9, u)
        bottom = hsf.step(-0.9, v)
        color *= left
        color *= bottom
        color *= line(0.4, 0.5, u, v)
        pixels[i, j] = color


gui = ti.GUI("Canvas", res=(res_x, res_y), fast_gui=True)

t = 0
while gui.running:
    t += 0.03
    render(t)
    gui.set_image(pixels)
    gui.show()
