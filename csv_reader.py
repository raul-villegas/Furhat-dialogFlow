import csv
import matplotlib.pyplot as plt

filename = "results.csv"  # replace with the actual filename

# Create empty lists to store data
conversations = []
conversation_lengths = []
fallback_rates = []
color_google = ['#f39c12', '#e74c3c', '#16a085', '#3498db', '#9b59b6']
color_default= ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#d3d3d3"]

# Open the CSV file and create a reader object
with open(filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    # Iterate over each row in the CSV file
    for row in reader:
        conversation_id = row["conversation_id"]
        conversation_length = int(row["conversation_length"])
        fallback_rate = float(row["fallback_rate"])

        # Add the conversation ID and length to the lists
        conversations.append(conversation_id)
        conversation_lengths.append(conversation_length)
        fallback_rates.append(fallback_rate)

# Set up the bar chart
fig, ax = plt.subplots()
ax.set_title("Conversation Lengths by Conversation")
ax.set_xlabel("Conversation ID")
ax.set_ylabel("Length")
ax.bar(conversations, conversation_lengths, color= color_google)

# # Show the bar chart
# plt.show()

# Set up the pie chart
fig, ax = plt.subplots()
ax.set_title("Fallback Rates by Conversation")
ax.pie(fallback_rates, labels=conversations, colors=color_google, autopct='%1.1f%%')

# Show both charts
plt.show()


