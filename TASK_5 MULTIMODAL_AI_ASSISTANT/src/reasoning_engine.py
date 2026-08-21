class ReasoningEngine:
    """
    Resolves contextual references using conversation history
    and previously extracted visual evidence.
    """

    def __init__(self, memory, context_manager):
        self.memory = memory
        self.context_manager = context_manager

    def reason(self, question):
        """
        Analyze the current question against previous context.
        """

        context = self.context_manager.get_relevant_context(
            question
        )

        analysis = context.get(
            "latest_image_analysis"
        )

        result = {
            "question": question,
            "has_context": bool(
                context.get("previous_messages")
            ),
            "has_reference": context.get(
                "has_contextual_reference",
                False
            ),
            "resolved_reference": None,
            "supporting_evidence": [],
            "reasoning": [],
            "confidence": 0.0
        }

        if not analysis:

            result["reasoning"].append(
                "No previous visual evidence is available."
            )

            return result

        question_lower = question.lower()

        objects = analysis.get(
            "objects",
            []
        )

        visible_text = analysis.get(
            "visible_text",
            []
        )

        relationships = analysis.get(
            "relationships",
            []
        )

        visual_features = analysis.get(
            "visual_features",
            []
        )

        # --------------------------------------------------
        # POSITIONAL REFERENCES
        # --------------------------------------------------

        ordinal_map = {
            "first": 0,
            "1st": 0,
            "second": 1,
            "2nd": 1,
            "third": 2,
            "3rd": 2,
            "fourth": 3,
            "4th": 3,
            "fifth": 4,
            "5th": 4
        }

        selected_index = None

        for word, index in ordinal_map.items():

            if word in question_lower:
                selected_index = index
                break

        if selected_index is not None:

            # Prefer visible text because this image contains
            # clearly ordered text labels.
            if selected_index < len(visible_text):

                selected_item = visible_text[
                    selected_index
                ]

                result[
                    "resolved_reference"
                ] = selected_item

                result[
                    "supporting_evidence"
                ].append(
                    f"Item {selected_index + 1}: "
                    f"{selected_item}"
                )

                result[
                    "reasoning"
                ].append(
                    f"The question refers to item "
                    f"{selected_index + 1}, which is "
                    f"'{selected_item}'."
                )

                result["confidence"] = 0.95

                return result

            elif selected_index < len(objects):

                selected_item = objects[
                    selected_index
                ]

                result[
                    "resolved_reference"
                ] = selected_item

                result[
                    "supporting_evidence"
                ].append(
                    f"Object {selected_index + 1}: "
                    f"{selected_item}"
                )

                result[
                    "reasoning"
                ].append(
                    f"The question refers to object "
                    f"{selected_index + 1}, which is "
                    f"'{selected_item}'."
                )

                result["confidence"] = 0.85

                return result

        # --------------------------------------------------
        # LAST / FINAL ITEM
        # --------------------------------------------------

        if any(
            phrase in question_lower
            for phrase in [
                "last one",
                "last item",
                "final one",
                "final item"
            ]
        ):

            if visible_text:

                selected_item = visible_text[-1]

                result[
                    "resolved_reference"
                ] = selected_item

                result[
                    "supporting_evidence"
                ].append(
                    f"Last visible text: {selected_item}"
                )

                result[
                    "reasoning"
                ].append(
                    f"The question refers to the "
                    f"last visible text item: "
                    f"'{selected_item}'."
                )

                result["confidence"] = 0.95

                return result

        # --------------------------------------------------
        # PRONOUN REFERENCES
        # --------------------------------------------------

        pronouns = [
            "it",
            "this",
            "that",
            "they",
            "them"
        ]

        contains_pronoun = any(
            word in question_lower.split()
            for word in pronouns
        )

        if contains_pronoun:

            # If previous user message explicitly mentioned
            # an entity, use that as the candidate.
            messages = self.memory.get_messages()

            for message in reversed(messages):

                text = message.get("text")

                if not text:
                    continue

                text_lower = text.lower()

                for item in (
                    visible_text +
                    objects
                ):

                    if item.lower() in text_lower:

                        result[
                            "resolved_reference"
                        ] = item

                        result[
                            "supporting_evidence"
                        ].append(
                            f"Previous conversation "
                            f"mentioned: {item}"
                        )

                        result[
                            "reasoning"
                        ].append(
                            f"The pronoun appears to "
                            f"refer to '{item}' based "
                            f"on the previous conversation."
                        )

                        result["confidence"] = 0.80

                        return result

            # If only one obvious object/text candidate exists,
            # it can be used as a weak reference.
            candidates = (
                visible_text +
                objects
            )

            if len(candidates) == 1:

                result[
                    "resolved_reference"
                ] = candidates[0]

                result[
                    "supporting_evidence"
                ].append(
                    f"Only clear candidate: "
                    f"{candidates[0]}"
                )

                result[
                    "reasoning"
                ].append(
                    "Only one clear visual candidate "
                    "was available."
                )

                result["confidence"] = 0.65

                return result

            result[
                "reasoning"
            ].append(
                "A contextual reference was detected, "
                "but there are multiple possible candidates."
            )

            result["confidence"] = 0.30

            return result

        # --------------------------------------------------
        # DIRECT EVIDENCE MATCH
        # --------------------------------------------------

        for item in (
            visible_text +
            objects +
            visual_features
        ):

            if item.lower() in question_lower:

                result[
                    "resolved_reference"
                ] = item

                result[
                    "supporting_evidence"
                ].append(
                    f"Question directly mentions: {item}"
                )

                result[
                    "reasoning"
                ].append(
                    f"The question directly references "
                    f"'{item}'."
                )

                result["confidence"] = 0.95

                return result

        # --------------------------------------------------
        # NO CLEAR REFERENCE
        # --------------------------------------------------

        result[
            "reasoning"
        ].append(
            "No specific visual reference could "
            "be confidently resolved."
        )

        result["confidence"] = 0.40

        return result