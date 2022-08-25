import matplotlib, numpy, sys, tkinter as Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
matplotlib.use('TkAgg')
canvas = None
fig = Figure
f = Figure(figsize=(3, 2), dpi=100)
ax = f.add_subplot(111)

rects = None


def create(root, data):
    global canvas, f, ax, rects

    ind = numpy.arange(len(data))  # the x locations for the groups
    width = .1

    ax.clear()
    ax.set_ylim(0, 1.0)
    ax.set_ylim(0, 1.0)
    ax.set_title('Targets')
    rects = ax.bar(ind, data, width)

    if canvas:
        canvas.get_tk_widget().pack_forget()
    canvas = FigureCanvasTkAgg(f, master=root)
# if canvas is not None:
#     for item in canvas.get_tk_widget().find_all():
#         canvas.get_tk_widget().delete(item)
    canvas.draw()

    canvas.get_tk_widget().pack()

#
# if __name__ == '__main__':
#     run(root)
