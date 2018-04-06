# encoding: utf-8

from pptx.util import (
    Emu,
    Pt,
    Cm,
    Inches)

import pandas as pd

# ----------------------------------------------------------------------------
# Font defaults

default_font_name='Trebuchet MS'
#default_font_file='fonts\Raleway-Regular.ttf'

default_font = {
    'font_name': default_font_name,
    'font_size': 9,
    'font_bold': False,
    'font_italic': False,
    'font_underline': False,
    'font_color': (89, 89, 89),
    'font_color_brightness': 0,
    'font_color_theme': None
}

# Chart Legend
default_font_legend = default_font.copy()

# Chart Category axis
default_font_caxis = default_font.copy()

# Chart Value axis
default_font_vaxis  = default_font.copy()
default_font_vaxis['font_bold'] = True

# Chart data labels
default_font_data_label  = default_font.copy()
default_font_data_label['font_size'] = 8.5
default_font_data_label['font_color'] = (0, 0, 0)

# ----------------------------------------------------------------------------
# Textframe defaults

default_textframe = {
    'fit_text': True,
    'margin_left': Cm(0.25),
    'margin_right': Cm(0.25),
    'margin_top': Cm(0.13),
    'margin_bottom': Cm(0.13),
    'vertical_alignment': 'top',
    'horizontal_alignment': 'left',
    'font_kwargs': default_font.copy()
}

# ---------------------------------------------------------------------------
# Textbox defaults
default_textbox = {
            'text': '',
            'left': Cm(2.31),
            'top': Cm(3.25),
            'width': Cm(29.23),
            'height': Cm(1.75),
            'rotation': 0,
            'textbox_fill_solid': False,
            'textbox_color': (100, 0, 0),
            'textbox_color_brightness': 0,
            'textframe_kwargs': default_textframe.copy()
}

# -------------------------------------------------------------------------------------------
# Chart defaults (Bar_clustered 1 series)

default_chart = {
    'dataframe': pd.DataFrame(),
    'chart_type': 'bar_clustered',
    'left': 838800, 'top': 1476000, 'width': 10515600, 'height': 4140000,
    'chart_style': 2,
    # Title
    'has_chart_title': False,
    'titletext': None,
    'textframe_kwargs': default_textframe.copy(),
    # Legend properties
    'has_legend': False,
    'legend_position': 'right',
    'legend_in_layout': False,  # will we ever set this True?
    'legend_horz_offset': 0.1583,
    # Category axis properties
    'caxis_visible': True,
    'caxis_tick_label_position': 'next_to_axis',
    'caxis_tick_labels_offset': 730,
    'caxis_has_major_gridlines': False,
    'caxis_has_minor_gridlines': False,
    'caxis_major_tick_mark': 'outside',
    'caxis_minor_tick_mark': 'none',
    # Value axis properties
    'vaxis_visible': True,
    'vaxis_tick_label_position': 'low',
    'vaxis_has_major_gridlines': True,
    'vaxis_has_minor_gridlines': False,
    'vaxis_major_tick_mark': 'outside',
    'vaxis_minor_tick_mark': 'none',
    'vaxis_max_scale': 1.0,
    'vaxis_min_scale': 0.0,
    'vaxis_major_unit': 0.1,
    'vaxis_minor_unit': None,
    'vaxis_tick_labels_num_format': '0%',
    'vaxis_tick_labels_num_format_is_linked': False,
    # Datalabel properties
    'plot_has_data_labels': True,
    'data_labels_position': 'outside_end',
    'data_labels_num_format': '0%',
    'data_labels_num_format_is_linked': False,
    # Plot properties
    'plot_vary_by_cat' : False,
    'plot_gap_width': 150,
    'plot_overlap': -10,
    # Number format
    'number_format': '0.00%',
    'xl_number_format': '0.00%'
}

#--------------------------
# Bar_Clustered 1 series
default_chart_bar = default_chart.copy()

#--------------------------
# Bar_Stacked_100%
default_chart_bar_stacked100 = default_chart.copy()
default_chart_bar_stacked100['chart_type'] = 'bar_stacked_100'
# Legend properties
default_chart_bar_stacked100['has_legend'] = True
default_chart_bar_stacked100['legend_horz_offset'] = 0
# Datalabel properties
default_chart_bar_stacked100['data_labels_position'] = 'center'
# Plot properties
# default_chart_bar_stacked100['plot_vary_by_cat'] = True
default_chart_bar_stacked100['plot_overlap'] = 100

#---------------------------
# Line
default_chart_line = default_chart.copy()
default_chart_line['chart_type'] = 'line'
# Category axis properties
default_chart_line['caxis_tick_label_position'] = 'low'
default_chart_line['caxis_tick_labels_offset'] = 100
# Datalabel properties
default_chart_line['data_labels_position'] = 'above'
# Plot properties
default_chart_line['plot_overlap'] = 10
default_chart_line['smooth_line'] = True

#----------------------------
# Column
default_chart_column = default_chart.copy()
default_chart_column['chart_type'] =  'column_clustered'
# Category axis properties
default_chart_column['caxis_tick_labels_offset'] = 730
# Plot properties
default_chart_column['plot_overlap'] = 10

#---------------------------
# Pie
default_chart_pie = default_chart.copy()
default_chart_pie['chart_type'] =  'pie'
# Legend properties
default_chart_pie['has_legend'] = True
default_chart_pie['legend_position'] = 'bottom'
# Plot properties
default_chart_pie['plot_vary_by_cat'] = True

#----------------------------
# Question_text-dict for default_slide_kwargs
question_text = default_textbox.copy()
question_text['left'] = 838800
question_text['top'] = 1026000
question_text['width'] = 10515600
question_text['height'] = 468000
question_text['textframe_kwargs'] = default_textframe.copy()
question_text['textframe_kwargs']['font_kwargs'] = default_font.copy()
question_text['textframe_kwargs']['font_kwargs']['font_size']=11
question_text['textframe_kwargs']['font_kwargs']['font_bold']=True
question_text['textframe_kwargs']['font_kwargs']['font_italic']=True

#----------------------------
# Base_description-dict for default_slide_kwargs
base_desc = default_textbox.copy()
base_desc['left'] = 838800
base_desc['top'] = 5652000
base_desc['width'] = 10515600
base_desc['height'] = 396000
base_desc['textframe_kwargs'] = default_textframe.copy()
base_desc['textframe_kwargs']['font_kwargs'] = default_font.copy()
base_desc['textframe_kwargs']['font_kwargs']['font_bold']=True

#----------------------------------------------------------------------------------------------
# Testing a version with dict in dicts 'txtboxes'/'chart' instead of list
default_slide_kwargs = {
    'textboxs': {},
    'charts': {},
}

