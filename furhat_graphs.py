import matplotlib.pyplot as plt
import numpy as np

# Define data for each conversation
conversations = {
    'Conversation 1': {'total_utterances': 100, 'fallbacks': 35},
    'Conversation 2': {'total_utterances': 150, 'fallbacks': 20},
    'Conversation 3': {'total_utterances': 200, 'fallbacks': 60},
    'Conversation 4': {'total_utterances': 75, 'fallbacks': 25},
}

# Calculate fallback rates for each conversation
fallback_rates = {}
for conversation, data in conversations.items():
    total_utterances = data['total_utterances']
    fallbacks = data['fallbacks']
    fallback_rate = fallbacks / total_utterances * 100
    fallback_rates[conversation] = fallback_rate

# Set up color scheme
color_palette = ['#f39c12', '#e74c3c', '#16a085', '#3498db', '#9b59b6']  
color_map = {conversation: color_palette[i] for i, conversation in enumerate(conversations.keys())}

# Create bar chart
fig, ax = plt.subplots()
x = np.arange(len(conversations))
ax.bar(x, fallback_rates.values(), color=[color_map[conversation] for conversation in conversations.keys()])
ax.set_xticks(x)
ax.set_xticklabels(conversations.keys(), rotation=45, ha='right')
ax.set_ylabel('Percentage')
ax.set_ylim([0, 100])
ax.set_title('Fallback Rates')
plt.tight_layout()

# Save chart to PNG file
plt.savefig('fallback_rates.png')

# Create pie chart
fig, ax = plt.subplots()
ax.pie(fallback_rates.values(), labels=conversations.keys(), colors=[color_map[conversation] for conversation in conversations.keys()], autopct='%1.1f%%')
ax.set_title('Fallback Rates')
plt.tight_layout()

# Save chart to PNG file
plt.savefig('fallback_rates_pie.png')


# Pastel colors: ['#f39c12', '#e74c3c', '#16a085', '#3498db', '#9b59b6']
# Bright and bold: ['#f1c40f', '#e67e22', '#e74c3c', '#3498db', '#9b59b6']