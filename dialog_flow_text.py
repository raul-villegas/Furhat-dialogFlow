import os
from google.cloud import dialogflow_v2 as dialogflow
import csv


# Set up credentials for accessing the Dialogflow API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "PATH TO JSON KEY"
# Set up a connection to the Dialogflow API
session_client = dialogflow.SessionsClient()
session_path = session_client.session_path("PROJECT NAME","PROJECT-ID")

# Check if the file exists and create it if it doesn't
if not os.path.exists('results.csv'):
    with open('results.csv', 'w', newline='') as csvfile:
        fieldnames = ['conversation_id', 'fallback_rate', 'user_utterances', 'conversation_length']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

# Read the last conversation ID from the CSV file
with open('results.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)
    if len(rows) > 1:
        last_id = rows[-1][0]
    else:
        last_id = '0'

# Initialize the utterance count and fallbacks
conversation_id = str(int(last_id) + 1)
user_utterances=0
fallbacks_count=0
bot_utterances=0

# Open a file for writing the conversation transcript
with open(f"conversation_transcript_{conversation_id}.txt", "w") as f:
    
    # Initialize list of intents used
    intents_used = []
    
    while True:
        # Prompt user for input
        text_input = input("You: ")
        f.write("User: " + text_input + "\n")

        # Increment the utterance count
        user_utterances += 1

        # Send a text query to the Dialogflow agent
        text_query_input = dialogflow.types.TextInput(text=text_input, language_code='en-US')
        query_input = dialogflow.types.QueryInput(text=text_query_input)
        response = session_client.detect_intent(session=session_path, query_input=query_input)

        # Append the detected intent to the intents list
        intent_name = response.query_result.intent.display_name
        if intent_name not in intents_used:
            intents_used.append(intent_name)

    #    if response.query_result.intent.display_name.lower() in end_conversation_intents:
    #        print("Conversation ended")
    #        break 
        if response.query_result.intent.end_interaction == True:
            print("Conversation end")
            break

        # Print the agent's response
        f.write("Bot: " + response.query_result.fulfillment_text + "\n")
        print("Bot: ", response.query_result.fulfillment_text)

        # Increment the utterance count
        bot_utterances += 1

        # Increment the fallbacks counter
        if "Fallback".lower() in response.query_result.intent.display_name.lower():
            fallbacks_count += 1
        

        # Iterate over the fulfillment messages and look for the "gesture" payload field
        message = response.query_result.fulfillment_messages

        if response.query_result.fulfillment_messages:
            for message in response.query_result.fulfillment_messages:
                if 'payload' in message:
                    payload = message.payload
                    if 'gesture' in payload:
                        gesture = payload['gesture']
                        # convert gesture to Gestures object, if necessary
                        # then call furhat.gesture(gesture)
                      #  print(gesture)

    
    # Calculations and evaluations
    fallback_rate= round((fallbacks_count / user_utterances)* 100,4)
    conversation_length= user_utterances + bot_utterances

    # Print the number of fallbacks
    print("Total Fallbacks: ", str(fallbacks_count))
    f.write("\nTotal Fallbacks: " + str(fallbacks_count))
    
    # Print the utterance count
    print("Total user utterances: ", user_utterances)
    f.write("\nTotal user utterances: " + str(user_utterances))

    # Print the fallback rate
    print("Fallback rate: ", fallback_rate, " %")
    f.write("\nFallback rate: " + str(fallback_rate))
    f.write(" %")

    # Print the conversation length
    print("Conversation length: ", conversation_length)
    f.write("\nConversation length: " + str(conversation_length))

    # print the list of intents used
    print("Intents used:", intents_used)
        
# Write the conversation data to the CSV file
with open('results.csv', 'a', newline='') as csvfile:
    fieldnames = ['conversation_id', 'fallback_rate', 'user_utterances', 'conversation_length']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if csvfile.tell() == 0:
        writer.writeheader()
    writer.writerow({'conversation_id': conversation_id, 'fallback_rate': fallback_rate, 'user_utterances': user_utterances, 'conversation_length': conversation_length})
