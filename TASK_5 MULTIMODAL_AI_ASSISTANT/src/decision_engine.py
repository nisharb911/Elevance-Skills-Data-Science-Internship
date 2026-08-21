class DecisionEngine:
    """
    Converts semantic validation results into a final
    assistant action.
    """

    def decide(
        self,
        validation_result,
        response,
        clarification=None
    ):

        decision = validation_result.get(
            "decision",
            "REJECT"
        )

        score = validation_result.get(
            "score",
            0.0
        )

        # ======================================================
        # ACCEPT
        # ======================================================

        if decision == "ACCEPT":

            return {
                "action": "ANSWER",

                "final_response": response,

                "confidence": score,

                "reason": (
                    "Response accepted because "
                    "evidence and reasoning provide "
                    "sufficient support."
                )
            }

        # ======================================================
        # QUALIFY
        # ======================================================

        if decision == "QUALIFY":

            qualified_response = (
                "Based on the available visual "
                "evidence, this appears to be: "
                f"{response}\n\n"
                "Note: This interpretation has "
                "some uncertainty because the "
                "available evidence is incomplete."
            )

            return {
                "action": "ANSWER_WITH_CAUTION",

                "final_response":
                    qualified_response,

                "confidence": score,

                "reason": (
                    "Response partially supported; "
                    "uncertainty has been explicitly "
                    "communicated."
                )
            }

        # ======================================================
        # CLARIFY
        # ======================================================

        if decision == "CLARIFY":

            return {
                "action": "CLARIFY",

                "final_response": (
                    clarification
                    or
                    "Could you clarify what you "
                    "are referring to?"
                ),

                "confidence": score,

                "reason": (
                    "The question is ambiguous and "
                    "the system should not guess."
                )
            }

        # ======================================================
        # REJECT
        # ======================================================

        return {
            "action": "REJECT",

            "final_response": (
                "I don't have enough reliable "
                "evidence to answer that confidently."
            ),

            "confidence": score,

            "reason": validation_result.get(
                "reason",
                "Insufficient evidence."
            )
        }