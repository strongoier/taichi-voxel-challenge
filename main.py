from scene import Scene
import taichi as ti
from taichi.math import *

N = 60
scene = Scene(voxel_edges=0, exposure=5)
scene.set_directional_light((-1, 1, 1), 0.01, (0.2, 0.2, 0.16))
scene.set_floor(-N, (1, 1, 1))
scene.set_background_color((0.2, 0.2, 0.16))

@ti.func
def gen_ellipsoid(r, a, center, color):
    for i, j, k in ti.ndrange((-r * a, r * a), (-r, r), (-r, r)):
        x = vec3(i / a, j, k)
        if x.dot(x) < r * r:
            scene.set_voxel(center + vec3(i, j, k), 1, color)

@ti.func
def gen_calabash(bottom_center, color):
    gen_ellipsoid(8, 1.2, bottom_center, color)
    gen_ellipsoid(5, 1.2, bottom_center + vec3(0, 12, 0), color)
    gen_ellipsoid(2, 1, bottom_center + vec3(0, 18, 0), color)
    ti.loop_config(serialize=True)
    for y in range(int(bottom_center.y) + 20, N):
        gen_ellipsoid(1, 1, vec3(bottom_center.x, y, bottom_center.z), vec3(0.2, 0.2, 0))

@ti.kernel
def initialize_voxels():
    gen_calabash(vec3(-50, -20, 20), vec3(0.9, 0, 0))
    gen_calabash(vec3(-40, 0, -30), vec3(0.9, 0.4, 0))
    gen_calabash(vec3(-20, -5, -30), vec3(0.9, 0.8, 0))
    gen_calabash(vec3(0, -10, 10), vec3(0.3, 0.6, 0))
    gen_calabash(vec3(10, -5, -20), vec3(0, 0.1, 0.5))
    gen_calabash(vec3(30, -20, 0), vec3(0, 0.5, 1))
    gen_calabash(vec3(40, 0, -30), vec3(0.5, 0.1, 1))

initialize_voxels()
scene.finish()
