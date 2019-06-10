# @author Kyle
# Copyright Kyle 2019
# Generates a plot of ups and downs in a given story structure
#bokeh code based on https://bokeh.pydata.org/en/1.0.0/docs/user_guide/examples/tools_hover_tooltip_formatting.html
import numpy as np

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure

from textblob import TextBlob
import matplotlib.pyplot as plt
import heapq

fileName = "t1.txt"

file = open(fileName)
text = TextBlob(file.read())
word_counts = text.word_counts

vals = []
nums = []
sents = []
i = 0

for thing in text.sentences:
    sents.append(thing)
    vals.append(thing.sentiment.polarity)
    nums.append(i)
    i = i + 1

# Thanks to ideas from https://medium.com/incedge/text-summarization-96079bf23e83
sentence_scores = {}
for sent in sents:
    count = 0
    words = sent.words
    for word in words:
        if word in word_counts:
            count += word_counts[word]
    sentence_scores[sent] = count


summary_sent = heapq.nlargest(15, sentence_scores, key=sentence_scores.get)

summ = []
for sent in summary_sent:
    summ.append(sents.index(sent))
    summ.sort()

vals = []
nums = []

for thing in summ:
    vals.append(sents[thing].sentiment.polarity)
    nums.append(thing)
    print sents[thing]

sent_list = []

for thing in nums:
    sent_list.append(str(sents[thing]))

output_file("sentiment_quantifier.html")

source = ColumnDataSource(data={
    'numsent'      : nums,
    'sent val' : vals,
    'sent list' : sent_list,
    })

p = figure(plot_height=250, x_axis_type="linear", tools="", toolbar_location=None,
           title="Sentiment Quantifier", sizing_mode="scale_width")
p.background_fill_color="#f5f5f5"
p.grid.grid_line_color="white"
p.xaxis.axis_label = 'Sentence Number'
p.yaxis.axis_label = 'Sentiment Polarity'
p.axis.axis_line_color = None

p.line(x='numsent', y='sent val', line_width=2, color='#ebbd5b', source=source)

p.add_tools(HoverTool(
    tooltips=[
        ( 'Sentence Number   :',   '@numsent{%1.4f}'            ),
        ( 'Sentiment Polarity:',  '@{sent val}{%1.4f}' ),
        ( 'Sentence          :', '@{sent list}{%s}' ),
    ],

    formatters={
        'numsent'      : 'printf',
        'sent val' : 'printf',
        'sent list' : 'printf',
    },
    mode='vline'
))

show(p)
