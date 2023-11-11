def handler(event, context):
    if event['request']['type'] == "IntentRequest":
        intent_name = event['request']['intent']['name']
        
        # Check for your specific intent and handle accordingly
        if intent_name == "SetAppointmentIntent":
            # Extract details and set the appointment
            # ...

            # Prepare response
            response = {
                # ... construct a response compatible with Alexa Skills Kit
            }
            return response
