def load_levels(filename):
    levels = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            
            level_data = {
                "h": int(parts[0]),
                "w": int(parts[1]),
                "c_start": (int(parts[2]), int(parts[3]), int(parts[4])),
                "c_end": (int(parts[5]), int(parts[6]), int(parts[7])),
                "angle": float(parts[8]),
                # Parse anchors from "0:0;0:2" to [(0,0), (0,2)]
                "anchors": [tuple(map(int, a.split(':'))) for a in parts[9].split(';')]
            }
            levels.append(level_data)
    return levels
def load_specific_level(n):
    all_levels = load_levels("levels.txt")
    return all_levels[n]
