from collections import OrderedDict


class IntentDetector:
    """
    Detects customer-service intent using multilingual semantic
    similarity against intent examples.

    This avoids maintaining separate intent classifiers for
    every supported language.
    """

    INTENTS = OrderedDict(
        {
            "order_status": [
                "Where is my order?",
                "What is the status of my order?",
                "मेरा ऑर्डर कहाँ है?",
                "माझी ऑर्डर कुठे आहे?",
                "મારું ઓર્ડર ક્યાં છે?",
            ],

            "delivery_time": [
                "When will my order arrive?",
                "How long will delivery take?",
                "मेरा ऑर्डर कब आएगा?",
                "माझी ऑर्डर कधी येईल?",
                "મારું ઓર્ડર ક્યારે આવશે?",
            ],

            "cancel_order": [
                "I want to cancel my order.",
                "Cancel my order.",
                "मेरा ऑर्डर रद्द करना है।",
                "माझी ऑर्डर रद्द करायची आहे.",
                "મારું ઓર્ડર રદ કરવું છે.",
            ],

            "refund": [
                "I want a refund.",
                "How can I get my money back?",
                "मुझे रिफंड चाहिए।",
                "मला रिफंड हवा आहे.",
                "મને રિફંડ જોઈએ છે.",
            ],

            "return_product": [
                "I want to return the product.",
                "How do I return an item?",
                "मुझे उत्पाद वापस करना है।",
                "मला उत्पादन परत करायचे आहे.",
                "મારે પ્રોડક્ટ પરત કરવું છે.",
            ],

            "change_address": [
                "I want to change my delivery address.",
                "Can I change the address?",
                "मुझे डिलीवरी पता बदलना है।",
                "मला डिलिव्हरीचा पत्ता बदलायचा आहे.",
                "મારે ડિલિવરી સરનામું બદલવું છે.",
            ],

            "payment_issue": [
                "My payment failed.",
                "There is a problem with payment.",
                "मेरा पेमेंट फेल हो गया।",
                "माझे पेमेंट फेल झाले.",
                "મારું પેમેન્ટ નિષ્ફળ ગયું.",
            ],

            "product_information": [
                "Tell me about the product.",
                "What are the product details?",
                "इस उत्पाद के बारे में बताएं।",
                "उत्पादनाची माहिती द्या.",
                "પ્રોડક્ટ વિશે માહિતી આપો.",
            ],

            "general_support": [
                "I need help.",
                "Can you help me?",
                "मुझे मदद चाहिए।",
                "मला मदत हवी आहे.",
                "મને મદદ જોઈએ છે.",
            ],
        }
    )

    def __init__(self, embedder):
        self.embedder = embedder

        self.intent_names = list(self.INTENTS.keys())

        self.intent_examples = []

        self.example_intents = []

        for intent, examples in self.INTENTS.items():
            for example in examples:
                self.intent_examples.append(example)
                self.example_intents.append(intent)

        self.embeddings = self.embedder.encode(
            self.intent_examples
        )

    def detect(self, text: str):
        query_embedding = self.embedder.encode_single(text)

        scores = self.embeddings @ query_embedding

        best_index = scores.argmax()

        best_score = float(scores[best_index])

        intent = self.example_intents[best_index]

        # Conservative ambiguity threshold.
        if best_score < 0.40:
            return {
                "intent": "ambiguous",
                "confidence": best_score,
            }

        return {
            "intent": intent,
            "confidence": best_score,
        }