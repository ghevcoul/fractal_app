
import math

import svgwrite

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

    return math.ceil(max(x_vals)), math.ceil(max(y_vals))

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
