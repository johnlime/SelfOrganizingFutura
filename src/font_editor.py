import svg_tool as st
import angeniol as som

polygon = []
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
for i in range(10):
    polygon.append(st.path_to_polygon(st.svg_path_reader("svg_fonts/" + str(i) + ".svg"), 10))
for i in range(1, len(polygon)):
    output = som.run(polygon[i - 1], polygon[i])
    for t in range(len(output)):
        tmp_file = open("../edited_fonts/numbers/" + str(i - 1) + "_to_" + str(i) + "_" + str(t) + ".svg", "w")
        tmp_file.write(st.convert_to_string([output[t]]))
        tmp_file.close()

for i in alphabet:
    polygon.append(st.path_to_polygon(st.svg_path_reader("svg_fonts/upper_" + str(i) + ".svg"), 10))
for i in range(1, len(polygon)):
    output = som.run(polygon[i - 1], polygon[i])
    for t in range(len(output)):
        tmp_file = open("edited_fonts/uppercase/" + alphabet[i - 1] + "_to_" + alphabet[i] + "_" + str(t) + ".svg", "w")
        tmp_file.write(st.convert_to_string([output[t]]))
        tmp_file.close()

for i in alphabet:
    polygon.append(st.path_to_polygon(st.svg_path_reader("svg_fonts/lower_" + str(i) + ".svg"), 10))
for i in range(1, len(polygon)):
    output = som.run(polygon[i - 1], polygon[i])
    for t in range(len(output)):
        tmp_file = open("edited_fonts/lowercase/" + alphabet[i - 1] + "_to_" + alphabet[i] + "_" + str(t) + ".svg", "w")
        tmp_file.write(st.convert_to_string([output[t]]))
        tmp_file.close()
