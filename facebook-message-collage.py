# Author: Mike Gloudemans
# Date: 12/28/2018

# Import a JSON file downloaded from Facebook, containing messages from a group conversation.
# Color-code messages by sender and format them to make them look like Messenger chat bubbles.
# To be used for an art collage.

import json
import datetime

from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

div_template = '''<div class=outer-message><div class="message {creator} {month}">{text}</div></div>\n'''

# Load JSON file
with open("message.json") as f:
    data = json.load(f)["messages"]

# Format messages
for message in data:
    message["sender_name"] = message["sender_name"].replace(" ", "-")
    message["month"] = datetime.datetime.fromtimestamp(message["timestamp_ms"] // 1000.0).month
    if datetime.datetime.fromtimestamp(message["timestamp_ms"] // 1000.0).year < 2018:
        message["month"] = 1

with open("modified-messages.html", "wb") as w:

    w.write(
    '''
    <style type="text/css">
    .container
    {
        column-count: 2;
        width:700px;
    }
    .outer-message
    {
        width:300px;
    }
    .message
    {
        margin:5px;
        padding-left:10px;
        padding-right:10px;
        padding-top:6px;
        padding-bottom:6px;
        font-family: Lucida Grande,Lucida Sans Unicode,Lucida Sans,Geneva,Verdana,sans-serif;
        font-size: 13px;
        background-color: coral;
        border-radius: 20px;
        color: white;
        display: inline-block;
    }
    .Mark-Gloudemans
    {
        background-color: #F35369;
    }
    .Monica-Semancik-Gloudemans
    {
        background-color: #F7923B;
    }
    .Mike-Gloudemans
    {
        background-color: #F5C33B;
    }
    .Meg-Gloudemans
    {
        background-color: #A3CE71;
    }
    .Derek-Gloudemans
    {
        background-color: #54C7EC;
    }
    .Jacob-Gloudemans
    {
        background-color: #0084FF;
    }
    .Nicole-Gloudemans
    {
        background-color: #8C72CB;
    }
    
    </style>
    <div class=container>
    '''
    )

    # For each month...
    for month in range(1, 13):
    
        # Write header for this month so I know what we're looking at
        w.write("<h3>Month {0}</h3>\n".format(month))
    
        month_messages = [message for message in data if message["month"] == month][::-1]

        # For each message...
        for mm in month_messages:
        
            if "sent" in mm["content"] and ("photo" in mm["content"] or "video" in mm["content"]):
                continue
            if "set the emoji" in mm["content"]:
                continue
            if "http" in mm["content"]:
                continue
            
            mm["content"] = mm["content"].encode('utf-8').decode("ascii", "ignore")
            if mm["content"] == "":
                continue
            
            # Just write an HTML div for that message
            # Make the div class include the original poster and the month in which it was posted
            
            w.write(div_template.format(creator=mm["sender_name"], month=mm["month"], text=mm["content"]))
    
    w.write('''
    </div>
    ''')