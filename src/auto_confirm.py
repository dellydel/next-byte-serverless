def handler(event, context):
    # Auto-confirm the user so they can log in immediately
    event['response']['autoConfirmUser'] = True
    
    # Auto-verify the email so no verification code is sent
    event['response']['autoVerifyEmail'] = True
    
    # (Optional) Auto-verify phone number if needed
    # event['response']['autoVerifyPhone'] = True

    return event