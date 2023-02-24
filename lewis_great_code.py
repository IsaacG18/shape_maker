import matplotlib.pyplot as plt
import numpy as np
import random
import math



def rotate_and_translate(points, angle, radial_distance):
    c, s = np.cos(angle), np.sin(angle)
    R = np.array(((c, -s), (s, c)))  # Rotation matrix
    transformed_points = np.dot(points, R)  # Perform matrix multiplication to transform points
    tx, ty = radial_distance * np.cos(angle), radial_distance * np.sin(angle)  # Offset points from origin
    transformed_points[:, 0] += tx
    transformed_points[:, 1] += ty
    return transformed_points


def plot_function(func, angle, radial_distance):
    x = np.linspace(-4, 4, NUMBER_OF_POINTS)
    y = func(x)
    points = np.column_stack((x, y))
    transformed_points = rotate_and_translate(points, angle, radial_distance)
    plt.scatter(transformed_points[:, 0], transformed_points[:, 1])


def plot_parametric_function(func, angle, radial_distance, t):
    x, y = func(t)
    points = np.column_stack((x, y))
    transformed_points = rotate_and_translate(points, angle, radial_distance)
    plt.scatter(transformed_points[:, 0], transformed_points[:, 1])


def get_start_end_points(func, angle, radial_distance):
    x = np.linspace(-4, 4, NUMBER_OF_POINTS)
    y = func(x)
    points = np.column_stack((x, y))
    transformed_points = rotate_and_translate(points, angle, radial_distance)
    start_point = (transformed_points[0, 0], transformed_points[0, 1])
    end_point = (transformed_points[NUMBER_OF_POINTS - 1, 0], transformed_points[NUMBER_OF_POINTS - 1, 1])
    return start_point, end_point


def get_start_end_points_para(func, angle, radial_distance, t):
    x, y = func(t)
    points = np.column_stack((x, y))
    transformed_points = rotate_and_translate(points, angle, radial_distance)
    start_point = (transformed_points[0, 0], transformed_points[0, 1])
    end_point = (transformed_points[NUMBER_OF_POINTS - 1, 0], transformed_points[NUMBER_OF_POINTS - 1, 1])
    return start_point, end_point


def get_v1(func, angle, radial_distance, t):
    x, y = func(t)
    points = np.column_stack((x, y))
    transformed_points = rotate_and_translate(points, angle, radial_distance)
    secondtolast_end_point = (transformed_points[NUMBER_OF_POINTS - 2, 0], transformed_points[NUMBER_OF_POINTS - 2, 1])
    end_point = (transformed_points[NUMBER_OF_POINTS - 1, 0], transformed_points[NUMBER_OF_POINTS - 1, 1])

    secondtolast_end_point = np.asarray(secondtolast_end_point)
    end_point = np.asarray(end_point)

    v1 = end_point - secondtolast_end_point
    normalized_v = v1 / np.sqrt(np.sum(v1 ** 2))
    return normalized_v


def get_v2(func, angle, radial_distance, t):
    x, y = func(t)
    points = np.column_stack((x, y))
    transformed_points = rotate_and_translate(points, angle, radial_distance)
    first_point = (transformed_points[0, 0], transformed_points[0, 1])
    second_point = (transformed_points[1, 0], transformed_points[1, 1])

    first_point = np.asarray(first_point)
    second_point = np.asarray(second_point)

    v2 = second_point - first_point
    normalized_v = v2 / np.sqrt(np.sum(v2 ** 2))
    return normalized_v



def semi_circle(t):
    r = 5
    x = r * np.cos(t)
    y = r * np.sin(t)
    return x, y


def s_shape(t):
    a = 10
    x = a * np.sin(t)
    y = a * (np.cos(t) - 1)
    return x, y


angle = random.uniform(0, 360)
angle = angle * np.pi / 180
radial_distance = 20
NUMBER_OF_POINTS = 10

plt.xlim(-40, 40)
plt.ylim(-40, 40)

t_1 = np.linspace(0, np.pi, NUMBER_OF_POINTS)
t_2 = np.linspace(0,  np.pi, NUMBER_OF_POINTS)
t = np.linspace(0, 10, NUMBER_OF_POINTS)


def orientLine(line, start, facing):
    rotation = np.array([[math.cos(facing * np.pi), math.sin(facing * np.pi)],
            [-math.sin(facing * np.pi), math.cos(facing * np.pi)]])
    return (line @ rotation) + (start - line[0])

def angle_between(v1, v2):
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def main():
    x, y = semi_circle(t_1)
    shape = [np.column_stack((x, y))]
    for i in range(1):
        x, y = semi_circle(t_2)
        temp_shape = np.column_stack((x, y))
        v1 = shape[-1][-1] - shape[-1][-2]
        v2 = temp_shape[1] - temp_shape[0]
        new_point = (v1) * random.randint(10, 30) + shape[-1][-1]
        theta = angle_between(v1, v2)
        print(theta)
        temp_shape = orientLine(temp_shape, new_point, theta)

        plt.scatter(shape[-1][:, 0], shape[-1][:, 1])
        plt.scatter(temp_shape[:, 0], temp_shape[:, 1])
        plt.scatter(new_point[0], new_point[1])
        plt.show()
    
    # scale_const = random.randint(10, 30)
    # p = scale_const * v1
    # plot_parametric_function(semi_circle, angle + 2 * np.pi / 3 , radial_distance, t_1)
    # v2 = get_v2(semi_circle, angle + 2 * np.pi / 3, radial_distance, t_1)
    # theta = np.arccos(np.dot(v1, v2))
    # rotationmatrix = np.array(((np.cos(2 * np.pi - theta),-np.sin(2 * np.pi - theta)),(np.sin(2 * np.pi - theta),np.cos(2 * np.pi - theta))))
    # x, y = semi_circle(t)
    # points = np.column_stack((x, y))
    # transformed_points = np.dot(points, rotationmatrix)
    # shift = p - points
    # transformed_points = orientLine(line, start, facing)
    # plt.scatter(transformed_points[:, 0], transformed_points[:, 1])
    # plt.show()

main()

# plot_parametric_function(semi_circle, angle, radial_distance, t_1)
# plot_parametric_function(s_shape, angle + 2 * np.pi / 3, radial_distance, t_2)
# plot_parametric_function(lambda t: (t, 5 * np.sqrt(t)), angle + 4 * np.pi / 3, radial_distance, t)

# start_point1, end_point1 = get_start_end_points_para(semi_circle, angle, radial_distance, t_1)
# print(start_point1)
# print(end_point1)

# plt.show()