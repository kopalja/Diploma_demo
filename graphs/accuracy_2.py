import matplotlib
import matplotlib.pyplot as plt
import numpy as np

font = {'family' : 'normal', 'size'   : 24}
matplotlib.rc('font', **font)


with open("/tmp/results.txt", "r") as f:
    lines = [float(l) for l in f.read().splitlines()]
    voc = lines[:4]
    detrac = lines[4:8]
    dev = lines[8:12]


full = np.arange(len(dev))  # the x locations for the groups
width = 0.2  # the width of the bars
fig, ax = plt.subplots()
rects1 = ax.bar(full - width, voc, width, label='PASCAL VOC')
rects2 = ax.bar(full, detrac, width, label='DETRAC')
rects3 = ax.bar(full + width, dev, width, label='Testing custom')


ax.set_ylabel('Cars + Trucks + Motorbikes AP(0.5)')
ax.set_xticks(full)
ax.set_xticklabels(('Mobilenet V1-9(300)', 'Mobilenet V1-6(300)', 'Mobilenet V1-3(300)', 'Mobilenet V1-0(300)'))
locs = ["upper left", "lower left", "center right"]
ax.legend(loc = locs[0], bbox_to_anchor=(0.2,1))


def autolabel(rects, xpos='center'):
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*2, 2), textcoords="offset points",  ha=ha[xpos], va='bottom')


autolabel(rects1, "center")
autolabel(rects2, "center")
autolabel(rects3, "center")
fig.tight_layout()
plt.show()