
### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta
from botocore.vendored import requests
import json


### Functionality Helper Functions ###
def parse_float(n):
    """
    Securely converts a non-numeric value to float.
    """
    try:
        return float(n)
    except ValueError:
        return float("nan")

def build_validation_result(is_valid, violated_slot, message_content):
    """
    Defines an internal validation message structured as a python dictionary.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}
    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }
def validate_data(crypto, crypto_var, time_length, intent_request):
    """
    Validates the data provided by the user.
    """
    # Validate that the user is over 21 years old
    if crypto is not None:
        valid_crypto = ["BTC", "ETH"]
        if crypto not in valid_crypto:
            return build_validation_result(
                False,
                "crypto",
                "Please enter valid crypto.",
            )
    if time_length is not None:
        valid_time = ["6 months", "1 year"]
        if time_length not in valid_time:
            return build_validation_result(
                False,
                "time_length",
                "Please enter valid time.",
            )
    # A True results is returned if age or amount are valid
    return build_validation_result(True, None, None)
### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]
def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """
    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }
def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """
    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }
def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """
    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }
    return response
    

def configure_message(crypto):
    message = "empty message"
    if crypto == "BTC":
        bitcoin_api_url = "https://api.alternative.me/v2/ticker/bitcoin/?convert=USD"
        response = requests.get(bitcoin_api_url)
        response_json = response.json()
        price_dollars = parse_float(response_json["data"]["1"]["quotes"]["USD"]["price"])
        message = f"""The price for BTC is {price_dollars}."""
    elif crypto == "ETH":
        ethereum_api_url = "https://api.alternative.me/v2/ticker/ethereum/?convert=USD"
        response = requests.get(ethereum_api_url)
        response_json = response.json()
        price_dollars = parse_float(response_json["data"]["1027"]["quotes"]["USD"]["price"])
        message = f"""The price for ETH is {price_dollars}."""
    return message
    
### Intents Handlers ###
def fetch_wallet_details(intent_request):
    """
    Performs dialog management and fulfillment for converting from dollars to bitcoin.
    """
    # Gets slots’ values
    wallet = get_slots(intent_request)["wallet"]
    # Gets the invocation source, for Lex dialogs “DialogCodeHook” is expected.
    source = intent_request["invocationSource"]  #
    if source == "DialogCodeHook":
        # This code performs basic validation on the supplied input slots.
        # Gets all the slots
        slots = get_slots(intent_request)
        # Validates user’s input using the validate_data function
        validation_result = validate_data(wallet, intent_request)
        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot
            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )
        # Fetch current session attributes
        output_session_attributes = intent_request["sessionAttributes"]
        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request))
    message = wallet_info(wallet)
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": message,
        },
    )

def fetch_crypto_details(intent_request):
    """
    Performs dialog management and fulfillment for converting from dollars to bitcoin.
    """
    # Gets slots’ values
    crypto = get_slots(intent_request)["crypto"]
    # Gets the invocation source, for Lex dialogs “DialogCodeHook” is expected.
    source = intent_request["invocationSource"]  #
    if source == "DialogCodeHook":
        # This code performs basic validation on the supplied input slots.
        # Gets all the slots
        slots = get_slots(intent_request)
        # Validates user’s input using the validate_data function
        validation_result = validate_data(crypto, intent_request)
        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot
            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )
        # Fetch current session attributes
        output_session_attributes = intent_request["sessionAttributes"]
        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request))
    message = configure_message(crypto)
    # Return a message with conversion’s result.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": message,
        },
    )

def fetch_ror_details(intent_request):
    """
    Performs dialog management and fulfillment for converting from dollars to bitcoin.
    """
    # Gets slots’ values
    crypto_var = get_slots(intent_request)["crypto_var"]
    time_length = get_slots(intent_request)["time_length"]
    # Gets the invocation source, for Lex dialogs “DialogCodeHook” is expected.
    source = intent_request["invocationSource"]  #
    if source == "DialogCodeHook":
        # This code performs basic validation on the supplied input slots.
        # Gets all the slots
        slots = get_slots(intent_request)
        # Validates user’s input using the validate_data function
        validation_result = validate_data(crypto_var, time_length, intent_request)
        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot
            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )
        # Fetch current session attributes
        output_session_attributes = intent_request["sessionAttributes"]
        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request))
    message = configure_ror_message(crypto_var, time_length)
    # Return a message with conversion’s result.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": message,
        },
    )

def configure_ror_message(crypto_var, time_length):
    message = "empty message"
    if crypto_var == "BTC" and time_length == "6 months":
        bitcoin_api_url_cg = "https://api.coingecko.com/api/v3/coins/bitcoin/history?date=14-02-2022"
        bitcoin_api_url = "https://api.alternative.me/v2/ticker/bitcoin/?convert=USD"
        response = requests.get(bitcoin_api_url)
        response_json = response.json()
        responsecg = requests.get(bitcoin_api_url_cg)
        responsecg_json = responsecg.json()
        price_dollars = parse_float(response_json["data"]["1"]["quotes"]["USD"]["price"])
        price_dollars_6mo = parse_float(responsecg_json["market_data"]["current_price"]["usd"])
        ror_btc = ((price_dollars - price_dollars_6mo)/price_dollars_6mo)*100
        message = f"""The rate of return for BTC over the last 6 months is {ror_btc}%."""
    elif crypto_var == "BTC" and time_length == "1 year":
        bitcoin_api_url_cg = "https://api.coingecko.com/api/v3/coins/bitcoin/history?date=14-07-2021"
        bitcoin_api_url = "https://api.alternative.me/v2/ticker/bitcoin/?convert=USD"
        response = requests.get(bitcoin_api_url)
        response_json = response.json()
        responsecg = requests.get(bitcoin_api_url_cg)
        responsecg_json = responsecg.json()
        price_dollars = parse_float(response_json["data"]["1"]["quotes"]["USD"]["price"])
        price_dollars_1yr = parse_float(responsecg_json["market_data"]["current_price"]["usd"])
        ror_btc = ((price_dollars - price_dollars_1yr)/price_dollars_1yr)*100
        message = f"""The rate of return for BTC over the last year is {ror_btc}%."""
    elif crypto_var == "ETH" and time_length == "6 months":
        ethereum_api_url_cg = "https://api.coingecko.com/api/v3/coins/ethereum/history?date=14-02-2022"
        ethereum_api_url = "https://api.alternative.me/v2/ticker/ethereum/?convert=USD"
        response = requests.get(ethereum_api_url)
        response_json = response.json()
        responsecg = requests.get(ethereum_api_url_cg)
        responsecg_json = responsecg.json()
        price_dollars = parse_float(response_json["data"]["1027"]["quotes"]["USD"]["price"])
        price_dollars_6mo = parse_float(responsecg_json["market_data"]["current_price"]["usd"])
        ror_eth = ((price_dollars - price_dollars_6mo)/price_dollars_6mo)*100
        message = f"""The rate of return for ETH over the last 6 months is {ror_eth}%."""
    elif crypto_var == "ETH" and time_length == "1 year":
        ethereum_api_url_cg = "https://api.coingecko.com/api/v3/coins/ethereum/history?date=14-07-2021"
        ethereum_api_url = "https://api.alternative.me/v2/ticker/ethereum/?convert=USD"
        response = requests.get(ethereum_api_url)
        response_json = response.json()
        responsecg = requests.get(ethereum_api_url_cg)
        responsecg_json = responsecg.json()
        price_dollars = parse_float(response_json["data"]["1027"]["quotes"]["USD"]["price"])
        price_dollars_1yr = parse_float(responsecg_json["market_data"]["current_price"]["usd"])
        ror_eth = ((price_dollars - price_dollars_1yr)/price_dollars_1yr)*100
        message = f"""The rate of return for ETH over the last year is {ror_eth}%."""
            
    return message

def wallet_info(wallet):
    if wallet == "yes":
        message = """Here are a couple digital wallet extensions. ---Gamestop Wallet Link--- https://chrome.google.com/webstore/detail/gamestop-wallet/pkkjjapmlcncipeecdmlhaipahfdphkd ---MetaMask Wallet --- https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn"""
        return message
    else:
        message = """Why would you use anything else?"""
        return message

### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """
    # Get the name of the current intent
    intent_name = intent_request["currentIntent"]["name"]
    # Dispatch to bot’s intent handlers
    if intent_name == "todaysPrice":
        return fetch_crypto_details(intent_request)
    elif intent_name == "digitalWallet":
        return fetch_wallet_details(intent_request)
    elif intent_name == "rateOfReturn":
        return fetch_ror_details(intent_request)
    raise Exception("Intent with name " + intent_name + " not supported")
### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    return dispatch(event)
