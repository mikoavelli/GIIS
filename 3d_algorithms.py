import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np
from tkinter import filedialog


def load_object(filename):
    vertices = []
    faces = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.split()
                if not parts:
                    continue
                if parts[0] == 'v':
                    vertices.append([float(x) for x in parts[1:4]] + [1])
                elif parts[0] == 'f':
                    faces.append([int(x.split('/')[0]) - 1 for x in parts[1:]])
        if not vertices or not faces:
            raise ValueError("The file does not contain any vertices or faces")
        return np.array(vertices, dtype=np.float32), faces
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")
    except ValueError as e:
        raise ValueError(f"Error when reading a file: {e}")


def apply_transformation(vertices, matrix):
    vertices_homogeneous = np.hstack((vertices[:, :3], np.ones((vertices.shape[0], 1))))
    transformed_vertices = np.dot(vertices_homogeneous, matrix.T)
    return transformed_vertices


def draw_object(vertices, faces):
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    for face in faces:
        for i in range(len(face)):
            glVertex3fv(vertices[face[i]][:3])
            glVertex3fv(vertices[face[(i + 1) % len(face)]][:3])
    glEnd()


def get_perspective_matrix(fov, aspect, near, far):
    f = 1.0 / np.tan(np.radians(fov) / 2.0)
    return np.array([[f / aspect, 0, 0, 0],
                     [0, f, 0, 0],
                     [0, 0, (far + near) / (near - far), 2 * far * near / (near - far)],
                     [0, 0, -1, 0]], dtype=np.float32)


def get_rotation_matrix(axis, angle):
    if axis == 'x':
        return np.array(
            [[1, 0, 0, 0], [0, np.cos(angle), -np.sin(angle), 0], [0, np.sin(angle), np.cos(angle), 0],
             [0, 0, 0, 1]], dtype=np.float32)
    if axis == 'y':
        return np.array(
            [[np.cos(angle), 0, np.sin(angle), 0], [0, 1, 0, 0], [-np.sin(angle), 0, np.cos(angle), 0],
             [0, 0, 0, 1]], dtype=np.float32)
    if axis == 'z':
        return np.array(
            [[np.cos(angle), -np.sin(angle), 0, 0], [np.sin(angle), np.cos(angle), 0, 0], [0, 0, 1, 0],
             [0, 0, 0, 1]], dtype=np.float32)
    return np.eye(4, dtype=np.float32)


def get_mirror_matrix(axis):
    if axis == 'x':
        return np.array([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.float32)
    if axis == 'y':
        return np.array([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.float32)
    if axis == 'z':
        return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]], dtype=np.float32)
    return np.eye(4, dtype=np.float32)


def choose_file():
    file_path = filedialog.askopenfilename(title="Select a 3D object file", filetypes=[("Text Files", "*.txt")])
    return file_path


def open_file_button_action():
    file_path = choose_file()
    if file_path:
        try:
            vertices, faces = load_object(file_path)
            print(f"The file {file_path} has been uploaded successfully.")
            open_gl_view(vertices, faces)
        except Exception as e:
            print(f"Error when uploading a file: {e}")


def open_gl_view(vertices, faces):
    pygame.init()
    display = (1600, 1200)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    glClearColor(1.0, 1.0, 1.0, 1.0)

    fov = 45
    aspect = display[0] / display[1]
    near = 0.1
    far = 50.0
    projection_matrix = get_perspective_matrix(fov, aspect, near, far)

    object_transformation = np.eye(4, dtype=np.float32)
    object_transformation[3][2] = -5

    rotation_speed = np.radians(150)
    last_time = pygame.time.get_ticks()

    mirror_x_triggered = False
    mirror_y_triggered = False
    mirror_z_triggered = False

    running = True
    while running:
        now_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        transformation = np.eye(4, dtype=np.float32)

        if keys[K_w] or keys[K_s] or keys[K_a] or keys[K_d] or keys[K_z] or keys[K_x]:
            delta_time = (now_time - last_time) / 1000.0
            angle = rotation_speed * delta_time
            if keys[K_w]:
                transformation = get_rotation_matrix('y', angle)
            if keys[K_s]:
                transformation = get_rotation_matrix('y', -angle)
            if keys[K_a]:
                transformation = get_rotation_matrix('x', angle)
            if keys[K_d]:
                transformation = get_rotation_matrix('x', -angle)
            if keys[K_z]:
                transformation = get_rotation_matrix('z', angle)
            if keys[K_x]:
                transformation = get_rotation_matrix('z', -angle)

        if keys[K_q]:
            scale_factor = 1.1
            transformation = np.array(
                [[scale_factor, 0, 0, 0], [0, scale_factor, 0, 0], [0, 0, scale_factor, 0], [0, 0, 0, 1]],
                dtype=np.float32)
        if keys[K_e]:
            scale_factor = 0.9
            transformation = np.array(
                [[scale_factor, 0, 0, 0], [0, scale_factor, 0, 0], [0, 0, scale_factor, 0], [0, 0, 0, 1]],
                dtype=np.float32)

        if keys[K_1] and not mirror_x_triggered:
            mirror_matrix = get_mirror_matrix('x')
            print("X-axis mirroring")
            transformation = np.dot(transformation, mirror_matrix)
            mirror_x_triggered = True

        elif keys[K_2] and not mirror_y_triggered:
            mirror_matrix = get_mirror_matrix('y')
            print("Y-axis mirroring")
            transformation = np.dot(transformation, mirror_matrix)
            mirror_y_triggered = True

        elif keys[K_3] and not mirror_z_triggered:
            mirror_matrix = get_mirror_matrix('z')
            print("Z-axis mirroring")
            transformation = np.dot(transformation, mirror_matrix)
            mirror_z_triggered = True

        if not keys[K_1]:
            mirror_x_triggered = False
        if not keys[K_2]:
            mirror_y_triggered = False
        if not keys[K_3]:
            mirror_z_triggered = False

        object_transformation = np.dot(transformation, object_transformation)
        transformed_vertices = apply_transformation(vertices, np.dot(object_transformation, projection_matrix))

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_object(transformed_vertices, faces)
        pygame.display.flip()
        pygame.time.wait(10)
        last_time = now_time

    pygame.quit()


def main():
    open_file_button_action()


if __name__ == "__main__":
    main()
