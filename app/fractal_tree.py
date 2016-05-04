"""
A recursive fractal tree builder.
"""
import math
import random

import svgwrite

# Values to use for non-random tree
DELTA_LENGTH = 0.61
DELTA_ANGLE = 45

# Random ranges to use
MIN_ANGLE = -65
MAX_ANGLE = 65
MIN_LENGTH = 0.45
MAX_LENGTH = 0.825
BRANCHES = [2, 2, 2, 3, 3, 3, 4, 5]

def build_tree(start=(0, 0), branch_len=150, angle=270, use_random=True):
    """
    A recursive function to build a fractal tree.

    Input:
    start - (x, y) tuple giving the starting point of the tree
    branch_len - the length of this branch of the tree

    Output:
    tree - list of (x1, y1, x2, y2) defining the line segments of this tree
    """
    if branch_len <= 3:
        return []
    else:
        tree = []
        x_end = start[0] + (branch_len * math.cos(math.radians(angle)))
        y_end = start[1] + (branch_len * math.sin(math.radians(angle)))
        tree.append((start[0], start[1], x_end, y_end))

        if use_random:
            for _ in range(random.choice(BRANCHES)):
                tree += build_tree(
                    (x_end, y_end),
                    branch_len * random.uniform(MIN_LENGTH, MAX_LENGTH),
                    angle + random.randrange(MIN_ANGLE, MAX_ANGLE),
                    use_random=use_random
                )
        else:
            r_angle = angle - DELTA_ANGLE
            l_angle = angle + DELTA_ANGLE
            r_len = branch_len * DELTA_LENGTH
            l_len = branch_len * DELTA_LENGTH
            # build the branches
            tree += build_tree((x_end, y_end), r_len, r_angle, use_random=use_random)
            tree += build_tree((x_end, y_end), l_len, l_angle, use_random=use_random)

        return tree

def tree_normalize(tree):
    """
    Takes a list of line segments defining a tree and normalizes them by 
    making all coordinates positive.
    """
    # Find the minimum x and y values
    x_vals = [(i[0], i[2]) for i in tree]
    x_vals = [item for sublist in x_vals for item in sublist]
    y_vals = [(i[1], i[3]) for i in tree]
    y_vals = [item for sublist in y_vals for item in sublist]

    x_shift = abs(min(x_vals))
    y_shift = abs(min(y_vals))

    # Add the shift values to each point
    new_tree = []
    for line in tree:
        new_tree.append((
            line[0] + x_shift,
            line[1] + y_shift,
            line[2] + x_shift,
            line[3] + y_shift
            ))
    return new_tree

def find_branch_length(branch):
    """
    Calculates the length of the given branch.
    """
    return math.sqrt((branch[2] - branch[0])**2 + (branch[3] - branch[1])**2)

def get_max_vals(tree):
    """
    Finds the max x and y values in the given tree and returns them.
    """
    x_vals = [(i[0], i[2]) for i in tree]
    x_vals = [item for sublist in x_vals for item in sublist]
    y_vals = [(i[1], i[3]) for i in tree]
    y_vals = [item for sublist in y_vals for item in sublist]

    return max(x_vals), max(y_vals)

def generate_svg(tree):
    """
    Takes a list of line segments defining a tree and builds the SVG for them.
    """
    tree = tree_normalize(tree)

    dwg = svgwrite.Drawing(size=get_max_vals(tree))

    # Add each branch to the drawing
    for branch in tree:
        width = math.floor(find_branch_length(branch) / 8)
        if width < 1:
            width = 1
        color = svgwrite.rgb(139, 69, 19)
        if find_branch_length(branch) < 6:
            color = svgwrite.rgb(34, 139, 34)
        dwg.add(dwg.line(
            start=branch[:2],
            end=branch[2:],
            stroke=color,
            stroke_width=width,
            stroke_linecap="round"
            ))
    # The linejoin parameter only works for shapes and polylines...
    #svgwrite.mixins.Presentation.stroke(dwg, linejoin="round")

    return dwg

def write_tree_file(tree, filename):
    """
    Takes a list of line segments defining a tree and writes them to an SVG file.
    """
    svg = generate_svg(tree)
    # Save the drawing
    svg.saveas(filename)

def get_tree_xml(tree):
    """
    Takes a list of line segments defining a tree and returns the XML
    for the SVG file as a string.
    """
    svg = generate_svg(tree)
    return svg.tostring()


if __name__ == "__main__":
    RANDOMIZED = False
    STARTLENGTH = 100
    TREE = build_tree((0, 0), STARTLENGTH, 270, use_random=RANDOMIZED)
    # write_tree(TREE, "test.svg")
    print(get_tree_xml(TREE))

