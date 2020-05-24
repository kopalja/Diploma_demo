### Description: Drawing the graphs presented in the thesis. 
### This script expect the input data to be stored in the "/tmp/results.txt" file


import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import argparse

font = {'family' : 'normal', 'size'   : 24}
matplotlib.rc('font', **font)



def create_graph(results, index, x_labels, bar_labels):
    if index == 5:
        data_1 = [lines[i] for i in range(len(lines)) if i % 3 == 0]
        data_2 = [lines[i] for i in range(len(lines)) if i % 3 == 1]
        data_3 = [lines[i] for i in range(len(lines)) if i % 3 == 2]  
    elif index == 4:
        data_1 = results[:3]
        data_2 = results[3:6]
        data_3 = results[6:9]
    elif index == 3:
        data_1 = results[:4]
        data_2 = results[4:8]
    else:
        data_1 = results[:4]
        data_2 = results[4:8]
        data_3 = results[8:12]


    full = np.arange(len(data_1))  # the x locations for the groups
    width = 0.2  # the width of the bars
    fig, ax = plt.subplots()

    ax.set_ylabel('Cars + Trucks + Motorbikes AP(0.5)')
    ax.set_xticks(full)
    ax.set_xticklabels(x_labels)

    rects1 = ax.bar(full - width, data_1, width, label=bar_labels[0])
    autolabel(rects1, ax, "center")

    rects2 = ax.bar(full, data_2, width, label=bar_labels[1])
    autolabel(rects2, ax, "center")
    
    if index != 3:
        rects3 = ax.bar(full + width, data_3, width, label=bar_labels[2])
        autolabel(rects3, ax, "center")


    locs = ["upper left", "lower left", "center right"]
    ax.legend(loc = locs[0], bbox_to_anchor=(0.25,1))
    fig.tight_layout()
    plt.show()

def autolabel(rects, ax,  xpos='center'):
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*2, 2), textcoords="offset points",  ha=ha[xpos], va='bottom')







if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph_index', type = int, help="Index of the graph to draw (1-5)")
    args = parser.parse_args()


    x_labels = [
        ['Mobilenet V1(300)', 'Retrained Mobilenet V1-6(300)', 'Mobilenet V2(300)', 'Retrained Mobilenet V2-6(300)'],
        ['Mobilenet V1-9(300)', 'Mobilenet V1-6(300)', 'Mobilenet V1-3(300)', 'Mobilenet V1-0(300)'],
        ['Mobilenet V2-7(300)', 'Mobilenet V2-7(360)', 'Mobilenet V2-7(420)', 'Mobilenet V2-7(540)'],
        ['Mobilenet V1-0(360)', 'Mobilenet V2-0(360)', 'Inception-0(360)'],
        ['Day-Night dataset', 'Day dataset', 'Night dataset']
    ]

    bar_labels = [
        ['PASCAL VOC', 'DETRAC', 'Testing custom'],
        ['PASCAL VOC', 'DETRAC', 'Testing custom'],
        ['DETRAC', 'Testing custom'],
        ['PASCAL VOC', 'DETRAC', 'Testing custom'],
        ['Day-Night model', 'Day model', 'Night model']
    ]

    # read generated results
    with open("/tmp/results.txt", "r") as f:
        lines = [float(l) for l in f.read().splitlines()]

    create_graph(lines, args.graph_index, x_labels[args.graph_index - 1], bar_labels[args.graph_index - 1])











