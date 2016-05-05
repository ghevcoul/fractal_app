"""
A recursive fractal tree builder.
"""
import sys
import math
import random
import time
from multiprocessing import Queue, JoinableQueue, Process


PARAMS = {
    "length": (0.45, 0.85),
    "angle": (-65, 65),
    "branches": [2, 2, 2, 3, 3, 3, 4, 4, 5]
}

def make_branch(start, length, angle):
    """
    Gets the x,y coordinates for the end of a branch with the input starting coordinates
    with branch length and angle.
    Returns a tuple of (x1, y1, x2, y2)
    """
    x_end = start[0] + (length * math.cos(math.radians(angle)))
    y_end = start[1] + (length * math.sin(math.radians(angle)))
    return (start[0], start[1], x_end, y_end)

def worker(work_q, res_q):

    while not work_q.empty():
        task = work_q.get()
        start, length, angle = task
        if length > 3:
            # Generate this branch
            branch = make_branch(start, length, angle)
            res_q.put(branch)
            # Put the next branches on the work queue
            next_pt = branch[2:]
            for _ in range(random.choice(PARAMS["branches"])):
                work_q.put(
                    (
                        next_pt,
                        length * random.uniform(PARAMS["length"][0], PARAMS["length"][1]),
                        angle + random.randrange(PARAMS["angle"][0], PARAMS["angle"][1])
                    )
                )
        work_q.task_done()

def build_tree_parallel(start=(0, 0), branch_len=150, angle=270):

    # Make a work queue and result queue
    work_queue = JoinableQueue()
    result_queue = Queue()

    # Put the first task in the work queue
    work_queue.put([start, branch_len, angle])

    # print(work_queue.get())
    # sys.exit()

    # Start a bunch of workers
    workers = 2
    processes = []
    for _ in range(workers):
        p = Process(target=worker, args=(work_queue, result_queue))
        p.start()
        processes.append(p)
        time.sleep(0.25)
    work_queue.join()
    # for p in processes:
    #     p.join()
    work_queue.close()

    # Collect the results...
    tree = []
    while not result_queue.empty():
        tree.append(result_queue.get())
    result_queue.close()
    print(len(tree))
    return tree


def build_tree(start=(0, 0), branch_len=150, angle=270):
    """
    A recursive function to build a fractal tree.

    Input:
    start - (x, y) tuple giving the starting point of the tree
    branch_len - the length of this branch of the tree

    Output:
    tree - list of (x1, y1, x2, y2) defining the line segments of this tree
    """
    params = {
        "length": (0.45, 0.825),
        "angle": (-65, 65),
        "branches": [2, 2, 2, 3, 3, 3, 4, 5]
    }

    if branch_len <= 3:
        return []
    else:
        tree = []
        branch = make_branch(start, branch_len, angle)
        tree.append(branch)

        for _ in range(random.choice(params["branches"])):
            tree += build_tree(
                (branch[2], branch[3]),
                branch_len * random.uniform(
                    params["length"][0],
                    params["length"][1]
                ),
                angle + random.randrange(params["angle"][0], params["angle"][1])
            )

        return tree



if __name__ == "__main__":
    # random.seed(1234)
    TREE = build_tree_parallel()

