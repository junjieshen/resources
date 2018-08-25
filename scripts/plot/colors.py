import brewer2mpl

mpl.rcParams['axes.color_cycle'] = colors

# A list of professional color combinations.
color_3 = ['pink', 'lightblue', 'lightgreen']
color_8 = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5']

np.random.seed(12)

# Change the default colors
#mpl.rcParams['axes.color_cycle'] =
colors = brewer2mpl.get_map('Set3', 'qualitative', 8).mpl_colors
