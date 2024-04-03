import mimetypes
import requests
import json

# ! Refreshes every 24 hours
bearer_token = "EABU7YlckmlkBOZBBgdw0CdhN11FE8yysjPAXZCGTFrYqq3HgjTzAglAs6CotyT4kIAZCpan99vOn66KLti6d0N6zZAveBWCcjC4oD9CZBxryCDdfIOOiDiBoJx56fg75oJCpAb1hNeRFvndmZCNMfGOXCwOfK4oQYRBb4VZCZA5YNHoSYJnMJjpOYD6pB2NiOgitTol2tCrZA5CRxV3ABRWtto6ZAdZAWEZD"

# ! Set to True if you have refreshed the token
refreshed = False


def SendMessage(text):
    """Sends the message to the WhatsApp number.

    Args
    ----
    - text: The message to be sent.
    """

    url = 'https://graph.facebook.com/v15.0/113814568315440/messages'
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }

    hardik = "9845072575"
    karan = "7348911401"
    harshit = "8058076999"

    number_name_map = {
        "9845072575": "Hardik",
        "7348911401": "Karan",
        "8058076999": "Harshit"
    }

    # List of recipients
    phone_list = [hardik, karan]
    for phone_number in phone_list:

        send_to = f"91{phone_number}"  # Start with 91 for Indian numbers

        # Prepare the data to be sent
        data = {
            "messaging_product": "whatsapp",
            "preview_url": False,
            "recipient_type": "individual",
            "to": send_to,
        }

        if refreshed:  # If token is refreshed, send a template message
            data["type"] = "template"
            data["template"] = {
                "name": "hello_world",
                "language": {
                    "code": "en_US"}
            }
        # If token is not refreshed, send an image message (normal message)
        else:
            data["type"] = "text"
            data["text"] = {
                "body": text
            }

        person_name = number_name_map[phone_number]
        print(f"Sending WhatsApp message to: {send_to} ({person_name})...")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Response content: {response.content}")
        print(f"✅ WhatsApp message sent to: {send_to} ({person_name})\n")
