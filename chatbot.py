
import re
import json
import random

# Sample FAQ dataset
FAQ_DATA = {
    "business_hours": {
        "patterns": [
            r"\b(business|working|office|opening)\s+hours\b",
            r"\bwhen.*(open|close)\b",
            r"\b(open|close)\s+time\b"
        ],
        "responses": [
            "Our business hours are Monday to Saturday, 9:00 AM to 6:00 PM."
        ]
    },
    "products": {
        "patterns": [
            r"\b(products|product list|catalog|catalogue)\b",
            r"\bwhat do you sell\b"
        ],
        "responses": [
            "We offer a range of products. Please tell me which product you want to know about."
        ]
    },
    "price": {
        "patterns": [
            r"\b(price|cost|how much)\b"
        ],
        "responses": [
            "Product prices depend on the item. Please provide the product name for more information."
        ]
    },
    "shipping": {
        "patterns": [
            r"\b(shipping|delivery|deliver|dispatch)\b"
        ],
        "responses": [
            "Delivery times depend on your location and product availability. Please contact our support team for order-specific details."
        ]
    },
    "returns": {
        "patterns": [
            r"\b(return|refund|exchange|replacement)\b"
        ],
        "responses": [
            "For returns or refunds, please keep your order details ready and contact our customer support team."
        ]
    },
    "contact": {
        "patterns": [
            r"\b(contact|phone number|email|support team)\b"
        ],
        "responses": [
            "You can contact the customer support team through the company's official website."
        ]
    },
    "thanks": {
        "patterns": [
            r"\b(thanks|thank you|thankyou)\b"
        ],
        "responses": [
            "You're welcome! Is there anything else I can help you with?"
        ]
    }
}


def normalize_text(text):
    """Convert input to lowercase and clean extra spaces."""
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def identify_intent(user_input):
    """Identify the user's intention using regular expressions."""
    text = normalize_text(user_input)

    for intent, details in FAQ_DATA.items():
        for pattern in details["patterns"]:
            if re.search(pattern, text):
                return intent

    return None


def get_response(user_input):
    """Generate a response based on the detected intent."""
    text = normalize_text(user_input)

    if re.fullmatch(r"(hi|hello|hey|good morning|good afternoon|good evening)[!. ]*", text):
        return "Hello! Welcome to Customer Support. How can I help you?"

    intent = identify_intent(text)

    if intent:
        return random.choice(FAQ_DATA[intent]["responses"])

    return (
        "Sorry, I didn't understand your question. "
        "You can ask about business hours, products, prices, "
        "delivery, returns, or contact information."
    )


def main():
    print("=" * 48)
    print("       CUSTOMER SUPPORT CHATBOT")
    print("=" * 48)
    print("Bot: Hello! How can I help you today?")
    print("Bot: Type 'bye', 'exit', or 'quit' to end the chat.")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Thank you for chatting. Goodbye!")
            break

        if not user_input:
            print("Bot: Please type a question.")
            continue

        if re.fullmatch(r"(bye|exit|quit)[!. ]*", normalize_text(user_input)):
            print("Bot: Thank you for chatting. Goodbye!")
            break

        response = get_response(user_input)
        print("Bot:", response)


if __name__ == "__main__":
    main()
