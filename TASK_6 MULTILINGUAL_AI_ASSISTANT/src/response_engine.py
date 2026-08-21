class ResponseEngine:
    """
    Generates controlled multilingual responses from retrieved
    knowledge and detected intent.

    This keeps answers consistent across languages.
    """

    RESPONSES = {
        "order_status": {
            "en": "Your order is currently being processed. You can check the latest status using your order details.",
            "hi": "आपका ऑर्डर अभी प्रोसेस किया जा रहा है। आप अपने ऑर्डर विवरण से नवीनतम स्थिति देख सकते हैं।",
            "mr": "तुमची ऑर्डर सध्या प्रक्रिया केली जात आहे. तुमच्या ऑर्डरच्या तपशीलातून नवीनतम स्थिती पाहू शकता.",
            "gu": "તમારો ઓર્ડર હાલમાં પ્રક્રિયામાં છે. તમે તમારા ઓર્ડરની વિગતો દ્વારા નવીનતમ સ્થિતિ તપાસી શકો છો.",
        },

        "delivery_time": {
            "en": "Delivery normally takes 3–5 business days.",
            "hi": "डिलीवरी में सामान्यतः 3–5 कार्यदिवस लगते हैं।",
            "mr": "डिलिव्हरीसाठी सामान्यतः 3–5 कामकाजाचे दिवस लागतात.",
            "gu": "ડિલિવરી માટે સામાન્ય રીતે 3–5 કામકાજના દિવસો લાગે છે.",
        },

        "cancel_order": {
            "en": "You can cancel the order if it has not yet been dispatched.",
            "hi": "यदि आपका ऑर्डर अभी डिस्पैच नहीं हुआ है, तो आप उसे रद्द कर सकते हैं।",
            "mr": "तुमची ऑर्डर अजून डिस्पॅच झाली नसेल तर तुम्ही ती रद्द करू शकता.",
            "gu": "જો તમારો ઓર્ડર હજી ડિસ્પેચ થયો નથી, તો તમે તેને રદ કરી શકો છો.",
        },

        "refund": {
            "en": "Refund requests can be submitted after the eligible order is cancelled or returned.",
            "hi": "योग्य ऑर्डर रद्द या वापस करने के बाद रिफंड अनुरोध किया जा सकता है।",
            "mr": "पात्र ऑर्डर रद्द किंवा परत केल्यानंतर रिफंडची विनंती करता येते.",
            "gu": "પાત્ર ઓર્ડર રદ અથવા પરત કર્યા પછી રિફંડની વિનંતી કરી શકાય છે.",
        },

        "return_product": {
            "en": "You can request a product return if the item meets the return policy.",
            "hi": "यदि उत्पाद रिटर्न नीति के अंतर्गत आता है, तो आप रिटर्न अनुरोध कर सकते हैं।",
            "mr": "उत्पादन रिटर्न पॉलिसीमध्ये पात्र असल्यास तुम्ही रिटर्नची विनंती करू शकता.",
            "gu": "જો ઉત્પાદન રિટર્ન નીતિ હેઠળ આવે છે, તો તમે રિટર્નની વિનંતી કરી શકો છો.",
        },

        "change_address": {
            "en": "You can change the delivery address before the order is dispatched.",
            "hi": "ऑर्डर डिस्पैच होने से पहले आप डिलीवरी पता बदल सकते हैं।",
            "mr": "ऑर्डर डिस्पॅच होण्यापूर्वी तुम्ही डिलिव्हरीचा पत्ता बदलू शकता.",
            "gu": "ઓર્ડર ડિસ્પેચ થાય તે પહેલાં તમે ડિલિવરી સરનામું બદલી શકો છો.",
        },

        "payment_issue": {
            "en": "Please verify your payment details and try again. If the issue continues, contact support.",
            "hi": "कृपया अपनी भुगतान जानकारी जांचकर दोबारा प्रयास करें। समस्या जारी रहने पर सपोर्ट से संपर्क करें।",
            "mr": "कृपया तुमचे पेमेंट तपशील तपासा आणि पुन्हा प्रयत्न करा. समस्या कायम राहिल्यास सपोर्टशी संपर्क करा.",
            "gu": "કૃપા કરીને તમારી ચુકવણીની વિગતો તપાસો અને ફરી પ્રયાસ કરો. સમસ્યા ચાલુ રહે તો સપોર્ટનો સંપર્ક કરો.",
        },

        "product_information": {
            "en": "Please provide the product name or product ID so I can help with the product details.",
            "hi": "कृपया उत्पाद का नाम या उत्पाद ID दें ताकि मैं उत्पाद की जानकारी दे सकूँ।",
            "mr": "कृपया उत्पादनाचे नाव किंवा उत्पादन ID द्या, म्हणजे मी उत्पादनाची माहिती देऊ शकतो.",
            "gu": "કૃપા કરીને પ્રોડક્ટનું નામ અથવા પ્રોડક્ટ ID આપો જેથી હું તેની માહિતી આપી શકું.",
        },

        "general_support": {
            "en": "Sure, I can help you. Please tell me what you need assistance with.",
            "hi": "ज़रूर, मैं आपकी मदद कर सकता हूँ। कृपया बताएं कि आपको किस चीज़ में सहायता चाहिए।",
            "mr": "नक्कीच, मी तुमची मदत करू शकतो. कृपया तुम्हाला कोणत्या गोष्टीत मदत हवी आहे ते सांगा.",
            "gu": "ચોક્કસ, હું તમારી મદદ કરી શકું છું. કૃપા કરીને તમને કઈ બાબતમાં મદદ જોઈએ છે તે જણાવો.",
        },

        "ambiguous": {
            "en": "I want to make sure I understand correctly. Could you please provide a little more detail?",
            "hi": "मैं सही तरीके से समझना चाहता हूँ। कृपया थोड़ा और विवरण दें।",
            "mr": "मला योग्य प्रकारे समजून घ्यायचे आहे. कृपया थोडी अधिक माहिती द्या.",
            "gu": "હું યોગ્ય રીતે સમજવા માંગું છું. કૃપા કરીને થોડી વધુ માહિતી આપશો?",
        },
    }

    def generate(
        self,
        intent: str,
        language_code: str,
        retrieved_results=None,
    ):
        if language_code not in {"en", "hi", "mr", "gu"}:
            language_code = "en"

        response_group = self.RESPONSES.get(
            intent,
            self.RESPONSES["general_support"]
        )

        return response_group.get(
            language_code,
            response_group["en"]
        )