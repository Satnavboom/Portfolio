import pygame
import numpy as np

# TYPES = "CUBE", "CONE", "SPHERE"
TYPE = "CUBE"
# MODES = "SINGLE", "TIME"
MODE = "TIME"
# COLORS = "<Vector3>" (e.g. (100, 255, 100)), "RAINBOW"
COLOR = "RAINBOW"
# FILLED = "TRUE", "FALSE"
FILLED = "TRUE"

pygame.init()

size = [2560, 1440]
window = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.SRCALPHA | pygame.SCALED)

fps_rate = 165

pygame.display.set_caption("3D Renderer")

black = (0, 0, 0)

def cube():
    vertices = np.array([
        [-1, -1, -1],
        [1, -1, -1],
        [1, 1, -1],
        [-1, 1, -1],
        [-1, -1, 1],
        [1, -1, 1],
        [1, 1, 1],
        [-1, 1, 1]
    ])

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Back face
        (4, 5), (5, 6), (6, 7), (7, 4),  # Front face
        (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
    ]
    
    return vertices, edges

def cone():
    num_base_points = 20
    radius = 2
    height = 3.5
    angle_step = 2 * np.pi / num_base_points
    
    base_vertices = []
    for i in range(num_base_points):
        angle = i * angle_step
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        base_vertices.append([x, y, 0])
    
    apex = [0, 0, height]
    
    vertices = np.array(base_vertices + [apex])
    
    # Center cone vertically
    vertices[:, 2] -= height / 4

    edges = []
    for i in range(num_base_points):
        edges.append((i, (i + 1) % num_base_points))
        edges.append((i, num_base_points))
    
    edges.append((num_base_points - 1, num_base_points))
    
    return vertices, edges

def sphere():
    latitude = 20
    longitude = 20
    radius = 2
    
    vertices = []
    edges = []
    
    for i in range(latitude + 1):
        theta = i * np.pi / latitude
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        
        for j in range(longitude):
            phi = j * 2 * np.pi / longitude
            x = radius * sin_theta * np.cos(phi)
            y = radius * sin_theta * np.sin(phi)
            z = radius * cos_theta
            vertices.append([x, y, z])
    
    vertices = np.array(vertices)
    
    for i in range(latitude):
        for j in range(longitude):
            curr = i * longitude + j
            nxt = curr + longitude
            
            edges.append((curr, nxt))
            edges.append((curr, (curr + 1) % longitude + i * longitude))
            edges.append((nxt, (nxt + 1) % longitude + (i + 1) * longitude))
            edges.append(((curr + 1) % longitude + i * longitude, (nxt + 1) % longitude + (i + 1) * longitude))

    return vertices, edges

def project_point(point, fov, viewer_distance):
    factor = fov / (viewer_distance + point[2])
    x = point[0] * factor + size[0] / 2
    y = -point[1] * factor + size[1] / 2
    return np.array([x, y])

def rotate_vertices(vertices, angle_x, angle_y):
    rotation_x = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])
    
    rotation_y = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])
    
    rotated_vertices = vertices.dot(rotation_x).dot(rotation_y)
    return rotated_vertices

def move(type, angle_x, angle_y, fov, viewer_distance):
    if type == "CUBE":
        viewer_distance = 3
        angle_x += 0.0035
        angle_y += 0.0035
    elif type == "CONE":
        angle_x = 1.4
        angle_y += 0.005
    elif type == "SPHERE":
        angle_x += 0.01
        angle_y += 0.01
    
    return angle_x, angle_y, fov, viewer_distance

# Shape updating for TIME mode
def update_shape(current_type, start_time, interval):
    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time > interval:
        shapes = ["CUBE", "CONE", "SPHERE"]
        next_type = shapes[(shapes.index(current_type) + 1) % len(shapes)]
        start_time = pygame.time.get_ticks()
        return next_type, start_time
    return current_type, start_time

def hsl_to_rgb(h, s, l):
    """ Convert HSL color to RGB. """
    def hue_to_rgb(p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1/6:
            return p + (q - p) * 6 * t
        if t < 1/2:
            return q
        if t < 2/3:
            return p + (q - p) * (2/3 - t) * 6
        return p
    
    if s == 0:
        r = g = b = l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)
    
    return (int(r * 255), int(g * 255), int(b * 255))

angle_x, angle_y = 0, 0
fov = 500
viewer_distance = 4

if TYPE == "CUBE":
    vertices, edges = cube()
elif TYPE == "CONE":
    vertices, edges = cone()
elif TYPE == "SPHERE":
    vertices, edges = sphere()

start_time = pygame.time.get_ticks()
interval = 5000 # Interval = seconds * 1000

# Smooth color transition parameters
color_change_speed = 0.0005
hue = 0

# Initialize the clock for FPS calculation
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 100)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if MODE == "TIME":
        TYPE, start_time = update_shape(TYPE, start_time, interval)
        if TYPE == "CUBE":
            vertices, edges = cube()
        elif TYPE == "CONE":
            vertices, edges = cone()
        elif TYPE == "SPHERE":
            vertices, edges = sphere()

    angle_x, angle_y, fov, viewer_distance = move(TYPE, angle_x, angle_y, fov, viewer_distance)
    rotated_vertices = rotate_vertices(vertices, angle_x, angle_y)
    
    # Clear screen
    window.fill(black)
    
    # Update hue for smooth color transition
    hue += color_change_speed
    if hue > 1:
        hue -= 1
    color = hsl_to_rgb(hue, 1, 0.5)  # Saturation and lightness set to 1 and 0.5 for vibrant colors
    
    # Draw edges
    for edge in edges:
        points = []
        for vertex in edge:
            projected_point = project_point(rotated_vertices[vertex], fov, viewer_distance)
            points.append(projected_point)
        pygame.draw.line(window, color, points[0], points[1], 1)
    
    # Calculate and display FPS
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
    window.blit(fps_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(fps_rate)
