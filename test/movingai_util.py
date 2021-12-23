from algorithms.structures import Map


def read_map_from_movingai_file(path, map_type=Map):
    with open(path, 'rt') as map_file:
        lines = list(map(
            lambda line: line.strip(),
            map_file.readlines()
        ))
        height = int(lines[1].split()[1])
        width = int(lines[2].split()[1])
        map_str = '\n'.join([
            ''.join(
                '#' if c != '.' else '.'
                for c in line
            )
            for line in lines[4:]
        ])
        task_map = map_type()
        task_map.read_from_string(map_str, width, height)
        return task_map


def read_tasks_from_movingai_file(path):
    tasks = []
    with open(path, 'rt') as map_file:
        lines = list(map(
            lambda line: line.strip(),
            map_file.readlines()
        ))[1:]
        for line in lines:
            _, _, _, _, start_j, start_i, goal_j, goal_i, result = line.split()
            tasks.append((int(start_i), int(start_j), int(goal_i), int(goal_j), float(result)))

    return tasks
