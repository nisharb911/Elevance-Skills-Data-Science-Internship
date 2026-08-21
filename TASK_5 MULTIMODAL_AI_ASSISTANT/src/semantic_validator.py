import re


class SemanticEvidenceValidator:
    """
    Performs lightweight semantic-style validation of a response
    against structured visual evidence.

    This layer does not blindly trust the generated response.
    It checks:
        1. Evidence coverage
        2. Reference consistency
        3. Unsupported claims
        4. Response confidence
    """

    def __init__(self):

        self.minimum_accept_score = 0.70
        self.minimum_qualify_score = 0.45

    # ==========================================================
    # TEXT NORMALIZATION
    # ==========================================================

    def _normalize(self, text):

        if not text:
            return ""

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # ==========================================================
    # EXTRACT EVIDENCE TERMS
    # ==========================================================

    def _extract_evidence_terms(
        self,
        visual_evidence
    ):

        terms = []

        fields = [
            "objects",
            "visible_text",
            "visual_features",
            "notable_conditions",
            "relationships"
        ]

        for field in fields:

            values = visual_evidence.get(
                field,
                []
            )

            if isinstance(values, list):

                for value in values:

                    if isinstance(value, str):

                        normalized = (
                            self._normalize(
                                value
                            )
                        )

                        if normalized:

                            terms.append(
                                normalized
                            )

        return list(
            dict.fromkeys(terms)
        )

    # ==========================================================
    # EVIDENCE COVERAGE
    # ==========================================================

    def _calculate_evidence_coverage(
        self,
        response,
        evidence_terms
    ):

        if not evidence_terms:

            return 0.0, []

        normalized_response = (
            self._normalize(
                response
            )
        )

        matched = []

        for term in evidence_terms:

            # Direct phrase match
            if term in normalized_response:

                matched.append(term)

        coverage = (
            len(matched)
            /
            len(evidence_terms)
        )

        return min(
            coverage,
            1.0
        ), matched

    # ==========================================================
    # REFERENCE CONSISTENCY
    # ==========================================================

    def _check_reference(
        self,
        response,
        reasoning_result
    ):

        reference = (
            reasoning_result.get(
                "resolved_reference"
            )
        )

        if not reference:

            return 1.0, True

        normalized_response = (
            self._normalize(
                response
            )
        )

        normalized_reference = (
            self._normalize(
                reference
            )
        )

        if (
            normalized_reference
            in normalized_response
        ):

            return 1.0, True

        return 0.20, False

    # ==========================================================
    # UNCERTAINTY CHECK
    # ==========================================================

    def _check_uncertainty(
        self,
        response,
        visual_evidence
    ):

        uncertainties = (
            visual_evidence.get(
                "uncertainties",
                []
            )
        )

        if not uncertainties:

            return 1.0

        uncertainty_words = [
            "uncertain",
            "unclear",
            "may",
            "might",
            "possibly",
            "appears",
            "cannot determine",
            "not enough information"
        ]

        normalized_response = (
            self._normalize(
                response
            )
        )

        for word in uncertainty_words:

            if word in normalized_response:

                return 1.0

        # If the image itself contains uncertainty
        # but the response speaks with absolute certainty,
        # reduce the score.

        return 0.60

    # ==========================================================
    # MAIN VALIDATION
    # ==========================================================

    def validate(
        self,
        response,
        visual_evidence,
        reasoning_result,
        ambiguity_result=None
    ):

        if not response:

            return {
                "decision": "REJECT",
                "valid": False,
                "score": 0.0,
                "reason": (
                    "No response was generated."
                ),
                "evidence_coverage": 0.0,
                "reference_consistency": 0.0,
                "matched_evidence": []
            }

        # ------------------------------------------------------
        # AMBIGUITY CHECK
        # ------------------------------------------------------

        if ambiguity_result:

            if ambiguity_result.get(
                "requires_clarification",
                False
            ):

                return {
                    "decision": "CLARIFY",
                    "valid": True,
                    "score": 1.0,
                    "reason": (
                        "The system detected unresolved "
                        "ambiguity and should request "
                        "clarification instead of guessing."
                    ),
                    "evidence_coverage": 1.0,
                    "reference_consistency": 1.0,
                    "matched_evidence": []
                }

        # ------------------------------------------------------
        # EVIDENCE
        # ------------------------------------------------------

        evidence_terms = (
            self._extract_evidence_terms(
                visual_evidence
            )
        )

        evidence_coverage, matched = (
            self._calculate_evidence_coverage(
                response,
                evidence_terms
            )
        )

        # ------------------------------------------------------
        # REFERENCE
        # ------------------------------------------------------

        reference_score, reference_supported = (
            self._check_reference(
                response,
                reasoning_result
            )
        )

        # ------------------------------------------------------
        # UNCERTAINTY
        # ------------------------------------------------------

        uncertainty_score = (
            self._check_uncertainty(
                response,
                visual_evidence
            )
        )

        # ------------------------------------------------------
        # REASONING CONFIDENCE
        # ------------------------------------------------------

        reasoning_confidence = (
            reasoning_result.get(
                "confidence",
                0.0
            )
        )

        # ------------------------------------------------------
        # FINAL SCORE
        # ------------------------------------------------------

        score = (
            (evidence_coverage * 0.35)
            +
            (reference_score * 0.30)
            +
            (uncertainty_score * 0.15)
            +
            (reasoning_confidence * 0.20)
        )

        score = round(
            min(score, 1.0),
            2
        )

        # ------------------------------------------------------
        # DECISION
        # ------------------------------------------------------

        if score >= self.minimum_accept_score:

            decision = "ACCEPT"

            reason = (
                "The response is sufficiently "
                "supported by the available evidence "
                "and contextual reasoning."
            )

            valid = True

        elif score >= self.minimum_qualify_score:

            decision = "QUALIFY"

            reason = (
                "The response has partial evidence "
                "support. It should be presented with "
                "appropriate uncertainty."
            )

            valid = True

        else:

            decision = "REJECT"

            reason = (
                "The response could not be "
                "sufficiently grounded in the "
                "available evidence."
            )

            valid = False

        # ------------------------------------------------------
        # REFERENCE OVERRIDE
        # ------------------------------------------------------

        if (
            not reference_supported
            and reasoning_result.get(
                "resolved_reference"
            )
        ):

            decision = "REJECT"

            valid = False

            reason = (
                "The generated response does not "
                "properly address the resolved "
                "reference."
            )

        return {
            "decision": decision,

            "valid": valid,

            "score": score,

            "reason": reason,

            "evidence_coverage":
                round(
                    evidence_coverage,
                    2
                ),

            "reference_consistency":
                round(
                    reference_score,
                    2
                ),

            "uncertainty_score":
                round(
                    uncertainty_score,
                    2
                ),

            "reasoning_confidence":
                round(
                    reasoning_confidence,
                    2
                ),

            "matched_evidence":
                matched
        }