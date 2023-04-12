import pandas as pd
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Read the conversation data from the CSV file
df = pd.read_csv('results.csv')

# Get the unique conversation IDs
conversations = df['conversation_id'].unique()

# Calculate the fallback rates for each conversation
fallback_rates = {conversation: df.loc[df['conversation_id'] == conversation, 'fallback_rate'].mean() for conversation in conversations}

# Calculate the conversation lengths for each conversation
conversation_lengths = df.groupby('conversation_id')['conversation_length'].sum()

# Set up color scheme
color_palette = ['#f39c12', '#e74c3c', '#16a085', '#3498db', '#9b59b6']
color_map = {conversation: color_palette[i % len(color_palette)] for i, conversation in enumerate(conversations)}
colors = [color_palette[i % len(color_palette)] for i in range(len(conversations))]

# Create bar chart
fig, ax = plt.subplots()
x = np.arange(len(conversations))
ax.bar(x, conversation_lengths.values, color=[color_map[conversation] for conversation in conversations])
ax.set_xticks(x)
ax.set_xticklabels(conversations, rotation=45, ha='right')
ax.set_ylabel('Conversation Length')
ax.set_title('Conversation Lengths')
plt.tight_layout()

# Create pie chart
fig, ax = plt.subplots()
ax.pie(fallback_rates.values(), labels=conversations, colors=colors, autopct='%1.1f%%')
ax.set_title('Fallback Rates')

# Show the chart
plt.show()

