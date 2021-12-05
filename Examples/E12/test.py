import matplotlib.pyplot as plt

files = ["jns_task01_3.ini", "jns_task01_4.ini", "jns_task01_5.ini", "lks_task01_3.ini", "lks_task01_4.ini", "lks_task01_5.ini"]
colors = ["r","g","b","c","m","y"]
x = [[],[],[],[],[],[]]
y = [[],[],[],[],[],[]]
for i, file in enumerate(files):
    data = []

    filename = file[file.rfind("\\")+1:]
    filename = filename[0:filename.find(".")]

    clean_values = []
    with open(file) as f:
        for line in f:
            clean_values.clear()
            for value in line.split(","):
                clean_values.append(float(value.rstrip()))
            data.append(clean_values.copy())

    for entry in data:
        x[i].append(entry[0])
        y[i].append(entry[1])
    plt.errorbar(x[i],y[i],color=colors[i],marker='x')
plt.show()