from collections import deque


def structure_parser(obj):
    structure = {}
    queue = deque([(k, v) for k, v in obj.items()])
    while len(queue) != 0:
        key, value = queue.popleft()
        structure[key] = list()
        if isinstance(value, dict):
            for k, v in value.items():
                structure[key].append(k)
                queue.append((k, v))

    return structure


def printer(structure, key, level, visited):
    if key in visited:
        return
    visited.add(key)
    print("    " * level, key)
    value = structure.get(key)
    if len(value) == 0:
        return
    else:
        for v in value:
            printer(structure, v, level + 1, visited)


def structure_printer(structure):
    visited = set()
    for k, v in structure.items():
        printer(structure, k, 0, visited)


def structure_summary(response):
    if isinstance(response, dict):
        structure = structure_parser(response)
        structure_printer(structure)
    if isinstance(response, list):
        structure = structure_parser(response[0])
        structure_printer(structure)
