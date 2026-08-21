from langdetect import detect, DetectorFactory, LangDetectException

DetectorFactory.seed = 0


class LanguageDetector:

    LANGUAGE_MAP = {
        "en": "English",
        "hi": "Hindi",
        "mr": "Marathi",
        "gu": "Gujarati",
    }

    ENGLISH_WORDS = {
        "the", "is", "are", "my", "your", "order",
        "where", "when", "what", "how", "can",
        "please", "want", "need", "cancel",
        "refund", "delivery", "address", "status",
        "change", "return", "payment", "product",
        "tell", "about", "still", "not"
    }

    DEVANAGARI_RANGE = range(
        0x0900,
        0x0980
    )

    GUJARATI_RANGE = range(
        0x0A80,
        0x0B00
    )

    def _contains_script(self, text, script_range):
        return any(
            ord(char) in script_range
            for char in text
        )

    def _contains_english_words(self, text):

        words = [
            word.lower().strip(".,!?;:")
            for word in text.split()
        ]

        return any(
            word in self.ENGLISH_WORDS
            for word in words
        )

    def detect_language(self, text: str) -> dict:

        text = text.strip()

        if not text:
            return {
                "code": "unknown",
                "language": "Unknown",
                "confidence": 0.0,
                "is_mixed": False,
            }

        has_devanagari = self._contains_script(
            text,
            self.DEVANAGARI_RANGE
        )

        has_gujarati = self._contains_script(
            text,
            self.GUJARATI_RANGE
        )

        has_english = self._contains_english_words(
            text
        )

        # Gujarati script has a strong signal.
        if has_gujarati:

            return {
                "code": "gu",
                "language": "Gujarati",
                "confidence": 0.98,
                "is_mixed": has_english,
            }

        # Devanagari + English indicates code mixing.
        if has_devanagari and has_english:

            try:
                detected = detect(text)
            except LangDetectException:
                detected = "hi"

            primary = (
                "hi"
                if detected not in {"mr", "hi"}
                else detected
            )

            return {
                "code": primary,
                "language": self.LANGUAGE_MAP.get(
                    primary,
                    "Hindi"
                ),
                "confidence": 0.92,
                "is_mixed": True,
            }

        # Pure Devanagari.
        if has_devanagari:

            try:
                detected = detect(text)
            except LangDetectException:
                detected = "hi"

            if detected not in {"hi", "mr"}:
                detected = "hi"

            return {
                "code": detected,
                "language": self.LANGUAGE_MAP[detected],
                "confidence": 0.94,
                "is_mixed": False,
            }

        # Normal language detection.
        try:
            detected = detect(text)
        except LangDetectException:
            detected = "unknown"

        language = self.LANGUAGE_MAP.get(
            detected,
            "Other"
        )

        if detected in self.LANGUAGE_MAP:
            confidence = 0.90
        else:
            confidence = 0.50

        return {
            "code": detected,
            "language": language,
            "confidence": confidence,
            "is_mixed": False,
        }

    def get_language_name(self, code):
        return self.LANGUAGE_MAP.get(
            code,
            "Unknown"
        )