import matplotlib
import matplotlib.pyplot as plt
import numpy as np



font = {'family' : 'normal','size'   : 24}
matplotlib.rc('font', **font)

with open("/tmp/results.txt", "r") as f:
    lines = [float(l) for l in f.read().splitlines()]
    day_night_model = [lines[i] for i in range(len(lines)) if i % 3 == 0]
    day_model = [lines[i] for i in range(len(lines)) if i % 3 == 1]
    night_model = [lines[i] for i in range(len(lines)) if i % 3 == 2]


full = np.arange(len(day_model))  # the x locations for the groups
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(full - width, day_night_model, width, label='Day-Night model')
rects2 = ax.bar(full, day_model, width, label='Day model')
rects3 = ax.bar(full + width, night_model, width, label='Night model')

# Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_yscale('log')
ax.set_ylabel('Cars + Trucks + Motorbikes AP(0.5)')
ax.set_xticks(full)
ax.set_xticklabels(('Day-Night dataset', 'Day dataset', 'Night dataset'))

locs = ["upper left", "lower left", "center right"]
ax.legend(loc = locs[0], bbox_to_anchor=(0.25,1))


def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*2, 2),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')


autolabel(rects1, "center")
autolabel(rects2, "center")
autolabel(rects3, "center")

fig.tight_layout()

plt.show()