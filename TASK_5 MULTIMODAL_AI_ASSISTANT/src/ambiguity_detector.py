class AmbiguityDetector:
    """
    Determines whether a reasoning result is sufficiently
    confident to continue or whether clarification is required.
    """

    def __init__(self, confidence_threshold=0.70):

        self.confidence_threshold = confidence_threshold

    def analyze(self, reasoning_result):

        confidence = reasoning_result.get(
            "confidence",
            0.0
        )

        has_reference = reasoning_result.get(
            "has_reference",
            False
        )

        resolved_reference = reasoning_result.get(
            "resolved_reference"
        )

        # --------------------------------------------------
        # CASE 1: CLEAR REFERENCE
        # --------------------------------------------------

        if (
            resolved_reference
            and confidence >= self.confidence_threshold
        ):

            return {
                "is_ambiguous": False,
                "requires_clarification": False,
                "confidence": confidence,
                "reason": (
                    "A clear reference was resolved "
                    "with sufficient confidence."
                ),
                "clarification_question": None
            }

        # --------------------------------------------------
        # CASE 2: CONTEXTUAL REFERENCE BUT LOW CONFIDENCE
        # --------------------------------------------------

        if has_reference:

            return {
                "is_ambiguous": True,
                "requires_clarification": True,
                "confidence": confidence,
                "reason": (
                    "A contextual reference was detected, "
                    "but it could not be resolved confidently."
                ),
                "clarification_question": None
            }

        # --------------------------------------------------
        # CASE 3: NO REFERENCE
        # --------------------------------------------------

        return {
            "is_ambiguous": False,
            "requires_clarification": False,
            "confidence": confidence,
            "reason": (
                "No unresolved contextual reference "
                "was detected."
            ),
            "clarification_question": None
        }

    def create_clarification_question(
        self,
        candidates
    ):
        """
        Generate a clarification question from
        possible visual candidates.
        """

        if not candidates:

            return (
                "Could you clarify what you are "
                "referring to?"
            )

        unique_candidates = []

        for candidate in candidates:

            if candidate not in unique_candidates:

                unique_candidates.append(candidate)

        candidate_text = ", ".join(
            unique_candidates
        )

        return (
            "Could you clarify which item you mean — "
            f"{candidate_text}?"
        )