import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the conversation data from the CSV file
df = pd.read_csv('results.csv')

# Get the unique conversation IDs
conversations = df['conversation_id'].unique()

# Calculate the fallback rates for each conversation
fallback_rates = {conversation: df.loc[df['conversation_id'] == conversation, 'fallback_rate'].mean() for conversation in conversations}

# Set up color scheme
color_palette = ['#f39c12', '#e74c3c', '#16a085', '#3498db', '#9b59b6']
color_map = {conversation: color_palette[i % len(color_palette)] for i, conversation in enumerate(conversations)}

# Create bar chart
fig, ax = plt.subplots()
x = np.arange(len(conversations))
ax.bar(x, fallback_rates.values(), color=[color_map[conversation] for conversation in conversations])
ax.set_xticks(x)
ax.set_xticklabels(conversations, rotation=45, ha='right')
ax.set_ylabel('Percentage')
ax.set_ylim([0, 100])
ax.set_title('Fallback Rates')
plt.tight_layout()
plt.show()

