def map_reader(map_num):
    # Read the data from the file
    with open(f'map{map_num}.txt', 'r') as file:
        lines = file.readlines()
    # Initialize lists for top, bottom, left, and right
    top = lines[0].split()
    bottom = lines[-1].split()
    left = []
    right = []

    for line in lines[1:-1]:
        left.append(line[0])
        right.append((line[-2]))

    top = list(map(int, top))
    bottom = list(map(int, bottom))
    left = list(map(int, left))
    right = list(map(int, right))

    return top, bottom, left, right