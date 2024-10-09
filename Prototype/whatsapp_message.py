import mimetypes
import requests
import json

# ! Refreshes every 24 hours
bearer_token = "EABU7YlckmlkBO8reKnEyrXYfYowL4pDfJGr70GOW7S2AVTc6YBpZC0tAkJ9jgGWrCX6BROmISka9BsVgZAPGvolnN0pkSTEclEvTGg6H9eSUC9ZC5EAdW2xUZCRgiqBZBa5fs7jaNNtwjcw4J7jsdRvlH12XTHCPWrFe8cZCwe4wpVmR8qR19r956ZA0UDh01DHCC9SNzJMyttGGeTyw2eVdFeM5Oxc8j5RA2N33wZDZD"


def SendMessage(text, refreshed=False):
    """Sends the message to the WhatsApp number.

    Args
    ----
    - `text`: The message to be sent.
    - `refreshed`: If the token is refreshed, set to True. It sends a template message. For normal message, set to False.
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
    phone_list = [hardik, karan, harshit]
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


if __name__ == "__main__":

    import time

    def test_whatsapp():

        # ! Set to True if you want to send a template message after refreshing the token
        send_template = True
        if send_template:
            print("Sending template message...")
            SendMessage("", refreshed=True)
            print("✅ Template message sent.\n")
            # Ask user if he received the message
            input("Did you receive the template message? Press Enter to continue...")
            print()

        print("Testing WhatsApp message...\n")

        # Test message
        start = time.time()
        message = "🧪 Hello! This is a test message from the WhatsApp bot to check the message functionality. No action is required from your end."
        SendMessage(message)
        end = time.time()
        print(f"✅ WhatsApp test completed in {end - start:.2f} seconds.")

    test_whatsapp()
