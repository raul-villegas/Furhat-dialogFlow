import os
from google.cloud import dialogflow_v2 as dialogflow
from furhat_remote_api import FurhatRemoteAPI
import time
from google.api_core.exceptions import InvalidArgument
import csv

## GOOGLE CREDENTIALS SET UP

# Set up credentials for accessing the Dialogflow API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
# Set up a connection to the Dialogflow API
session_client = dialogflow.SessionsClient()
session_path = session_client.session_path("","")

## FURHAT REMOTE API SET UP

# Create an instance of the FurhatRemoteAPI class, providing the address of the robot or the SDK running the virtual robot
furhat = FurhatRemoteAPI("localhost")

# Get the voices on the robot
voices = furhat.get_voices()

# Get the gestures on the robot
gestures = furhat.get_gestures()

# Set the voice of the robot
furhat.set_voice(name='Matthew')

# Get the users detected by the robot 
users = furhat.get_users()

# Attend the user closest to the robot
furhat.attend(user="CLOSEST")

# Set the LED lights
furhat.set_led(red=50, green=50, blue=200)

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
# Initialize the utterance count and fallbacks
user_utterances=0
fallbacks_count=0
bot_utterances=0

# Open a file for writing the conversation transcript
with open("dialogue_transcript.txt", "w") as f:

    while True:
            try:
                # Listen to user speech and return ASR result
                response_furhat = furhat.listen()
                text_input = response_furhat.message

                # Print user input and writes it on a file
                print("User: ", text_input)
                f.write("User: " + text_input + "\n")

                # Increment the utterance count
                user_utterances += 1
                
                # Send a text query to the Dialogflow agent
                text_query_input = dialogflow.types.TextInput(text=text_input, language_code='en-US')
                query_input = dialogflow.types.QueryInput(text=text_query_input)
                response = session_client.detect_intent(session=session_path, query_input=query_input)

                #Check if the response includes an "endconversation" intent
                if response.query_result.intent.end_interaction == True:
                    print("Conversation end")
                    break
                
                # Function to get the gesture from the custom payload from DialogFlow
                message = response.query_result.fulfillment_messages
                if response.query_result.fulfillment_messages:
                    for message in response.query_result.fulfillment_messages:
                        if 'payload' in message:
                            payload = message.payload
                            if 'gesture' in payload:
                                gesture = payload['gesture']
                                
                                try:
                                    # convert gesture to Gestures object, if necessary then call furhat.gesture(gesture)
                                    if gesture is not None:
                                        print("Gesture:", gesture)
                                        furhat.gesture(name=gesture)
                                        time.sleep(2)   

                                except Exception as e:
                                    print(f"Error performing gesture: {e}")            
                                    
                            else:
                                print("Gesture name not provided")
                                            
                furhat.listen_stop()
                furhat.say(text=response.query_result.fulfillment_text)

                # Print the agent's response
                f.write("Bot: " + response.query_result.fulfillment_text + "\n")
                print("Bot: ", response.query_result.fulfillment_text)

                # Increment the utterance count
                bot_utterances += 1
                
                # Increment the fallbacks counter       
                if "Fallback".lower() in response.query_result.intent.display_name.lower():
                    fallbacks_count += 1
                
                print(response.query_result.intent.display_name)    #Just to see the intent
                


                # Wait for the agent's response to finish before listening again
                time.sleep(len(response.query_result.fulfillment_text) / 10)
            
            except InvalidArgument:
                # If there is no voice input, skip to the next iteration of the loop
                continue

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
    
# Write the conversation data to the CSV file
with open('results.csv', 'a', newline='') as csvfile:
    fieldnames = ['conversation_id', 'fallback_rate', 'user_utterances', 'conversation_length']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if csvfile.tell() == 0:
        writer.writeheader()
    writer.writerow({'conversation_id': conversation_id, 'fallback_rate': fallback_rate, 'user_utterances': user_utterances, 'conversation_length': conversation_length})

 
