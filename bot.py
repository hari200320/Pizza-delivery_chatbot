from flask import Flask, request, jsonify
from groq import Groq
import os
import re

app = Flask(__name__)

# Configure Groq API
client = Groq(api_key='add_your_api_key')

conversation_state = {}
pizza_options = ["Margherita", "Pepperoni", "Veggie", "Paneer"]

def generate_response(user_input):
    pizza_context = (
        "You are a virtual assistant specifically designed for a pizza delivery service. "
        "Your goal is to provide helpful and accurate responses to any inquiries related to pizza orders, "
        "menu items, and delivery options. Here are some common questions you might receive:\n\n"
        "1. Ordering:\n"
        "- 'How do I place an order for a pizza?'\n"
        "- 'Can I customize my pizza toppings?'\n\n"
        "2. Menu Information:\n"
        "- 'What types of pizzas do you have?'\n"
        "- 'Do you offer gluten-free crust options?'\n\n"
        "3. Delivery Details:\n"
        "- 'What is the estimated delivery time for my order?'\n"
        "- 'How much is the delivery fee?'\n\n"
        "4. Payment and Confirmation:\n"
        "- 'What payment methods do you accept?'\n"
        "- 'Will I receive a confirmation once I place my order?'\n\n"
        "5. Special Offers:\n"
        "- 'Are there any current deals or discounts?'\n"
        "- 'Do you have any combo offers available?'\n\n"
        "6. Order Tracking:\n"
        "- 'How can I track my pizza delivery?'\n"
        "- 'What do I do if my order is late?'\n\n"
        "7. Cancellations and Complaints:\n"
        "- 'How can I cancel my order?'\n"
        "- 'What should I do if my pizza arrived cold?'\n\n"
        "8. Customer Feedback:\n"
        "- 'How can I leave feedback about my experience?'\n"
        "- 'Do you have a satisfaction guarantee?'\n\n"
        "Please remember to assist customers effectively with their pizza delivery inquiries."
    )

    # Create the request data structure
    request_data = {
        "messages": [
            {"role": "system", "content": pizza_context},
            {"role": "user", "content": user_input}
        ],
        "model": "llama3-8b-8192"
    }

    try:
        response = client.chat.completions.create(**request_data)
        return response.choices[0].message.content if response and response.choices else "I'm here to assist with pizza delivery inquiries only."
    except Exception as e:
        print(f"Error: {e}")
        return "I'm here to assist with pizza delivery inquiries only."

def is_pizza_related(user_input):
    pizza_keywords = [
        "pizza", "order", "delivery", "toppings", "size", "crust", "extra", "slices",
        "menu", "checkout", "address", "phone", "payment", "confirmation", "restaurant",
        "pickup", "time", "hours", "special", "deal", "discount", "custom", "items", 
        "ingredients", "order status", "delivery time", "delivery fee", "tracking", 
        "location", "cancellation", "reviews", "feedback", "hot", "cold", "fresh", 
        "delivery options", "order online", "pizza types", "availability", "special offers",
        "customer service", "refund", "complaints", "satisfaction", "reviews", "recommendations",
        "offers", "coupons", "combo", "side dishes", "beverages", "pickup time"
    ]
    return any(keyword.lower() in user_input.lower() for keyword in pizza_keywords)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    user_id = request.json.get('id')

    if user_id not in conversation_state:
        conversation_state[user_id] = {'order': {}}

    if not is_pizza_related(user_input):
        return jsonify({"response": "I'm here to assist with pizza delivery inquiries only."})

    response = generate_response(user_input)
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
