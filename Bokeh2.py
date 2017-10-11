from bokeh.io import curdoc, output_file, show
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool, Button, RadioGroup, Toggle, CheckboxGroup, Select, Slider, Tabs, CategoricalColorMapper
from bokeh.layouts import widgetbox, column, row, gridplot
from bokeh.palettes import Spectral6
# from bokeh.charts import BoxPlot
# from bokeh.server.server import Server
# from bokeh.embed import autoload_server
# from bokeh.client import push_session

import pandas as pd

# open a session to keep our local document in sync with server
# session = push_session(curdoc())


data = pd.read_csv('gapminder_tidy.csv', index_col = 'Year')

print(data.info())
print(data.head())

# Make the ColumnDataSource
source = ColumnDataSource(data={
                          'x'       : data.loc[1970].fertility,
                          'y'       : data.loc[1970].life,
                          'country'      : data.loc[1970].Country,
                          #    'pop'      : (data.loc[1970].population / 20000000) + 2,
                          'region'      : data.loc[1970].region
                          })

# Save the minimum and maximum values of the fertility column
xmin, xmax = min(data.fertility), max(data.fertility)

# Save the minimum and maximum values of the life expectancy column
ymin, ymax = min(data.life), max(data.life)

# Create the figure
plot = figure(title='Gapminder Data for 1970', plot_height=400, plot_width=700,
              x_range=(xmin, xmax), y_range=(ymin, ymax))

# Add circle glyphs to the plot
# plot.circle(x='x', y='y', fill_alpha=0.8, source=source_2)

# Set the x-axis label
plot.xaxis.axis_label ='Fertility (children per woman)'

# Set the y-axis label
plot.yaxis.axis_label = 'Life Expectancy (years)'

# Add the plot to the current document and add a title
# curdoc().add_root(plot)
# curdoc().title = 'Gapminder'

# output_file('gapminder_2.html')
# show(plot)

# Make a list of the unique values from the region column
regions_list = data.region.unique().tolist()

# Make a color mapper
color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)

# output_file('gapminder_2.html')
# show(plot)

# Make a slider object
slider = Slider(start = 1970, end = 2010, step = 1, value = 1970, title = 'Year')

# Define the callback function
def update_plot(attr, old, new):
    
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    
    new_data = {
        'x'       : data.loc[yr][x],
        'y'       : data.loc[yr][y],
        'country' : data.loc[yr].Country,
        #        'pop'     : (data.loc[yr].population / 20000000) + 2,
        'region'  : data.loc[yr].region
    }
    source.data = new_data

# Set the range of all axes
    plot.x_range.start = min(data[x])
    plot.x_range.end = max(data[x])
    plot.y_range.start = min(data[y])
    plot.y_range.end = max(data[y])
    
    # Add title to figure
    plot.title.text = 'Gapminder data for %d' % yr

# Add the color mapper to the circle glyph
plot.circle(x='x', y='y', fill_alpha=0.8, source=source,
            color=dict(field='region', transform=color_mapper), legend='region')

# Set the legend.location attribute of the plot
plot.legend.location = 'bottom_left'

# Attach the callback to the 'value' property of slider
slider.on_change('value',update_plot)

# Create a HoverTool
hover = HoverTool(tooltips = [('Country', '@country')])

# Add the HoverTool to the plot
plot.add_tools(hover)

# Create a dropdown Select widget for the x data
x_select = Select(
                  options=['fertility', 'life', 'child_mortality', 'gdp'],
                  value='fertility',
                  title='x-axis data'
                  )

# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data
y_select = Select(
                  options=['fertility', 'life', 'child_mortality'],
                  value='life',
                  title='y-axis data'
                  )

# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update_plot)

layout = row(widgetbox(slider,x_select,y_select), plot)

# output_file('gapminder.html')
# show(layout)
curdoc().add_root(layout)

# curdoc().add_periodic_callback(update_plot, 50)

# script = autoload_server(layout, session_id=session.id)
# print(script)

# session.show(layout) # open the document in a browser

# session.loop_until_closed() # run forever