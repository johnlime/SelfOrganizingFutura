from lxml import etree as et
import copy

""" Save font path to path_saves """
def svg_path_reader (svg_path):
    raw_path = et.parse(svg_path).getroot().findall('.//{http://www.w3.org/2000/svg}path')[0].get('d').split()
    path_saves = []
    current_index = -1
    for i in range(len(raw_path)):
        # command is included in slot
        if raw_path[i].isdigit() == False:
            # look for command. keep track of index of last command
            last_command = -1
            for j in range(len(raw_path[i])):
                if raw_path[i][j].isdigit() == False and raw_path[i][j] != '-' and raw_path[i][j] != '.': # new command found
                    if j != 0 and j - (last_command + 1) != 0:
                        # save value from after last command to current command
                        path_saves[current_index].append(float(raw_path[i][last_command + 1:j]))
                    # make new slot within path_saves. current_index is the number of commands
                    path_saves.append([])
                    current_index += 1
                    path_saves[current_index].append(raw_path[i][j])
                    last_command = j
                elif j == len(raw_path[i]) - 1:
                    # save the last value in slot
                    path_saves[current_index].append(float(raw_path[i][last_command + 1:]))
        # only 1 number is included in slot
        else:
            path_saves[current_index].append(float(raw_path[i]))
    return path_saves

""" Convert from curve to polygons """
def path_to_polygon (path_saves, definition = 100):
    path_polygon = [[]]
    current_index = 0
    prev_ctrl = [0, 0]
    current_pos = [0, 0]
    for key in path_saves:
        if key[0] == 'M': # move to
            path_polygon[current_index].append(key)
            current_pos[0] = key[1]
            current_pos[1] = key[2]

        elif key[0] == 'l': # line to
            x_seg = key[1] / definition
            y_seg = key[2] / definition
            for i in range(definition):
                path_polygon[current_index].append(['l', x_seg, y_seg])
            prev_ctrl[0] = 0
            prev_ctrl[1] = 0

        elif key[0] == 'h': # horizontal line to
            x_seg = key[1] / definition
            for i in range(definition):
                path_polygon[current_index].append(['l', x_seg, 0])
            prev_ctrl[0] = 0
            prev_ctrl[1] = 0

        elif key[0] == 'v': # horizontal line to
            y_seg = key[1] / definition
            for i in range(definition):
                path_polygon[current_index].append(['l', 0, y_seg])
            prev_ctrl[0] = 0
            prev_ctrl[1] = 0

        elif key[0] == 'q': # quadratic Bezier
            prev_x_seg = 0
            prev_y_seg = 0
            for tx in range(definition):
                t = 1/definition * tx
                x_seg = 2 * t * (1-t) * key[1] + t * t * key[3]
                y_seg = 2 * t * (1-t) * key[2] + t * t * key[4]
                path_polygon[current_index].append(['l', x_seg - prev_x_seg, y_seg - prev_y_seg])
                prev_x_seg = x_seg
                prev_y_seg = y_seg
            prev_ctrl[0] = key[3] - key[1]
            prev_ctrl[1] = key[4] - key[2]

        elif key[0] == 't': # smooth quadratic Bezier
            prev_x_seg = prev_y_seg = 0
            for tx in range(definition):
                t = 1/definition * tx
                x_seg = 2 * t * (1-t) * prev_ctrl[0] + t * t * key[1];
                y_seg = 2 * t * (1-t) * prev_ctrl[1] + t * t * key[2];
                path_polygon[current_index].append(['l', x_seg - prev_x_seg, y_seg - prev_y_seg])
                prev_x_seg = x_seg
                prev_y_seg = y_seg
            prev_ctrl[0] = key[1] - prev_ctrl[0]
            prev_ctrl[1] = key[2] - prev_ctrl[1]

        elif key[0] == 'z': # end current path
            path_polygon.append([])
            current_index += 1

        else: # error for unknown command
            raise NameError('Unknown command: ' + key)

    del path_polygon[-1]
    return path_polygon

def convert_to_string (path_polygon):
    output_string = "<?xml version=\"1.0\" standalone=\"no\"?><!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\" \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\" >"
    output_string += "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" version=\"1.1\" viewBox=\"-10 0 692 1000\">"
    output_string += "<g transform=\"matrix(1 0 0 -1 0 800)\">"
    output_string += "<path stroke=\"black\" fill=\"none\" d=\""
    for i in range(len(path_polygon)):
        for j in range(len(path_polygon[i])):
            for key in path_polygon[i][j]:
                output_string += str(key) + " "
    output_string += "\" /> </g> </svg>"
    return output_string
