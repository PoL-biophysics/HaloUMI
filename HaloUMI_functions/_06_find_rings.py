import numpy as np


def find_rings(vertex, centre_x, centre_y, plate_radius):

    dx = vertex[0] - centre_x
    dy = vertex[1] - centre_y

    deadzone_ring_x, deadzone_ring_y = (centre_x + 1.25 * dx), (centre_y + 1.25 * dy)
    dead_ring_vertex = [deadzone_ring_x, deadzone_ring_y]

    lawn_ring_x, lawn_ring_y = (centre_x + 3 * dx), (centre_y + 3 * dy)

    lawn_ring_hypotenuse = np.sqrt((lawn_ring_x - plate_radius) ** 2 + (lawn_ring_y - plate_radius) ** 2)

    if lawn_ring_hypotenuse < (4/5) * plate_radius:
        lawn_ring_vertex = [lawn_ring_x, lawn_ring_y]
    else:
        lawn_ring_vertex = None

    return lawn_ring_vertex, dead_ring_vertex