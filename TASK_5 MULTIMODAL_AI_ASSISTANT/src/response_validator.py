class ResponseValidator:
    """
    Validates whether a generated response is sufficiently
    grounded in the available evidence.
    """

    def __init__(self, minimum_confidence=0.70):

        self.minimum_confidence = minimum_confidence

    def validate(
        self,
        response,
        visual_evidence,
        reasoning_result
    ):
        """
        Validate the generated response.
        """

        response_lower = response.lower()

        confidence = reasoning_result.get(
            "confidence",
            0.0
        )

        resolved_reference = reasoning_result.get(
            "resolved_reference"
        )

        evidence_terms = []

        # ---------------------------------------------
        # COLLECT EVIDENCE TERMS
        # ---------------------------------------------

        for key in [
            "objects",
            "visible_text",
            "visual_features",
            "notable_conditions",
            "relationships"
        ]:

            values = visual_evidence.get(
                key,
                []
            )

            for value in values:

                if isinstance(value, str):

                    evidence_terms.append(
                        value.lower()
                    )

        # ---------------------------------------------
        # CHECK EVIDENCE MENTION
        # ---------------------------------------------

        matched_terms = []

        for term in evidence_terms:

            if term in response_lower:

                matched_terms.append(term)

        # ---------------------------------------------
        # REFERENCE CHECK
        # ---------------------------------------------

        reference_supported = True

        if resolved_reference:

            reference_supported = (
                resolved_reference.lower()
                in response_lower
            )

        # ---------------------------------------------
        # VALIDATION DECISION
        # ---------------------------------------------

        if not response.strip():

            return {
                "valid": False,
                "confidence": 0.0,
                "reason": "The generated response is empty.",
                "matched_evidence": []
            }

        if (
            resolved_reference
            and not reference_supported
        ):

            return {
                "valid": False,
                "confidence": 0.30,
                "reason": (
                    "The response does not appear to "
                    "address the resolved reference."
                ),
                "matched_evidence": matched_terms
            }

        # ---------------------------------------------
        # EVIDENCE-BASED RESPONSE
        # ---------------------------------------------

        if matched_terms:

            validation_confidence = min(
                1.0,
                0.70 + (
                    0.05 * len(matched_terms)
                )
            )

            return {
                "valid": True,
                "confidence": validation_confidence,
                "reason": (
                    "The response contains terms "
                    "supported by the visual evidence."
                ),
                "matched_evidence": matched_terms
            }

        # ---------------------------------------------
        # CONTEXTUAL ANSWER
        # ---------------------------------------------

        if confidence >= self.minimum_confidence:

            return {
                "valid": True,
                "confidence": 0.70,
                "reason": (
                    "The response is supported by "
                    "high-confidence contextual reasoning."
                ),
                "matched_evidence": []
            }

        # ---------------------------------------------
        # INSUFFICIENT EVIDENCE
        # ---------------------------------------------

        return {
            "valid": False,
            "confidence": 0.35,
            "reason": (
                "The response could not be sufficiently "
                "grounded in the available evidence."
            ),
            "matched_evidence": matched_terms
        }