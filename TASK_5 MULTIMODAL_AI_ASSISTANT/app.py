import streamlit as st
from PIL import Image

# ============================================================
# PROJECT MODULES
# ============================================================

from src.image_analyzer import ImageAnalyzer
from src.conversation_memory import ConversationMemory
from src.context_manager import ContextManager
from src.reasoning_engine import ReasoningEngine
from src.ambiguity_detector import AmbiguityDetector
from src.response_generator import ResponseGenerator
from src.response_validator import ResponseValidator

# Step 8 modules
from src.semantic_validator import SemanticEvidenceValidator
from src.decision_engine import DecisionEngine


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Multimodal AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "conversation_memory" not in st.session_state:

    st.session_state.conversation_memory = (
        ConversationMemory()
    )


memory = st.session_state.conversation_memory


# ============================================================
# INITIALIZE SYSTEM COMPONENTS
# ============================================================

context_manager = ContextManager(
    memory
)


reasoning_engine = ReasoningEngine(
    memory,
    context_manager
)


ambiguity_detector = AmbiguityDetector(
    confidence_threshold=0.70
)


# Step 8
semantic_validator = (
    SemanticEvidenceValidator()
)


decision_engine = (
    DecisionEngine()
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "🤖 Multimodal AI Assistant"
)

st.markdown(
    """
    A multimodal conversational AI assistant capable of
    understanding **text and images**, maintaining context,
    reasoning over visual evidence, handling ambiguity,
    validating responses, and making evidence-based decisions.
    """
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🧠 Conversation")

    st.write(
        f"Messages stored: **{memory.count()}**"
    )

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        memory.clear()

        st.rerun()


# ============================================================
# IMAGE UPLOAD
# ============================================================

st.subheader(
    "🖼️ Upload an Image"
)

uploaded_image = st.file_uploader(
    "Choose an image",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp"
    ],
    help="Upload an image for visual analysis."
)


image = None


if uploaded_image is not None:

    try:

        image = Image.open(
            uploaded_image
        )

        st.success(
            "Image uploaded successfully."
        )

        st.image(
            image,
            caption="Uploaded Image",
            width="stretch"
        )

    except Exception as e:

        st.error(
            f"Unable to read image: {e}"
        )


# ============================================================
# USER QUESTION
# ============================================================

st.subheader(
    "💬 Ask a Question"
)

user_question = st.text_area(
    "Enter your question",
    placeholder=(
        "Examples:\n"
        "• What does this image contain?\n"
        "• What does the third one represent?\n"
        "• What about the last one?\n"
        "• Is it important?"
    ),
    height=120
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.divider()

analyze_clicked = st.button(
    "🔍 Analyze",
    type="primary",
    use_container_width=True
)


# ============================================================
# MAIN PROCESSING
# ============================================================

if analyze_clicked:

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    if (
        image is None
        and not user_question.strip()
    ):

        st.warning(
            "Please upload an image, enter a question, "
            "or provide both."
        )

        st.stop()


    # ========================================================
    # CASE 1 — IMAGE PROVIDED
    # ========================================================

    if image is not None:

        try:

            # =================================================
            # IMAGE ANALYSIS
            # =================================================

            with st.spinner(
                "🔎 Analyzing image..."
            ):

                analyzer = ImageAnalyzer()

                analysis = analyzer.analyze(
                    image=image,
                    question=user_question.strip()
                )


            # =================================================
            # SAVE USER MESSAGE
            # =================================================

            memory.add_message(
                role="user",
                text=(
                    user_question.strip()
                    if user_question.strip()
                    else None
                ),
                image_name=(
                    uploaded_image.name
                    if uploaded_image
                    else None
                )
            )


            # =================================================
            # SAVE IMAGE ANALYSIS
            # =================================================

            memory.add_message(
                role="assistant",
                image_analysis=analysis
            )


            st.success(
                "Image analysis completed successfully."
            )


            # =================================================
            # VISUAL EVIDENCE
            # =================================================

            st.subheader(
                "🔎 Visual Evidence"
            )


            col1, col2 = st.columns(2)


            # -------------------------------------------------
            # OBJECTS
            # -------------------------------------------------

            with col1:

                st.write(
                    "### Objects"
                )

                st.write(
                    analysis.get(
                        "objects",
                        []
                    )
                )


                st.write(
                    "### Visual Features"
                )

                st.write(
                    analysis.get(
                        "visual_features",
                        []
                    )
                )


                st.write(
                    "### Visible Text"
                )

                st.write(
                    analysis.get(
                        "visible_text",
                        []
                    )
                )


            # -------------------------------------------------
            # OTHER VISUAL INFORMATION
            # -------------------------------------------------

            with col2:

                st.write(
                    "### Notable Conditions"
                )

                st.write(
                    analysis.get(
                        "notable_conditions",
                        []
                    )
                )


                st.write(
                    "### Relationships"
                )

                st.write(
                    analysis.get(
                        "relationships",
                        []
                    )
                )


                st.write(
                    "### Uncertainties"
                )

                st.write(
                    analysis.get(
                        "uncertainties",
                        []
                    )
                )


            # =================================================
            # VISUAL CONFIDENCE
            # =================================================

            visual_confidence = (
                analysis.get(
                    "overall_confidence",
                    0.0
                )
            )


            st.metric(
                "Visual Analysis Confidence",
                f"{visual_confidence:.0%}"
            )


            # =================================================
            # STRUCTURED ANALYSIS
            # =================================================

            with st.expander(
                "📋 View Structured Analysis"
            ):

                st.json(
                    analysis
                )


            # =================================================
            # QUESTION PROCESSING
            # =================================================

            if user_question.strip():

                question = (
                    user_question.strip()
                )


                # =============================================
                # CONTEXT
                # =============================================

                context = (
                    context_manager
                    .get_relevant_context(
                        question
                    )
                )


                # =============================================
                # REASONING
                # =============================================

                reasoning_result = (
                    reasoning_engine
                    .reason(
                        question
                    )
                )


                # =============================================
                # AMBIGUITY DETECTION
                # =============================================

                ambiguity_result = (
                    ambiguity_detector
                    .analyze(
                        reasoning_result
                    )
                )


                # =============================================
                # CANDIDATES FOR REFERENCE
                # =============================================

                candidates = []

                candidates.extend(
                    analysis.get(
                        "visible_text",
                        []
                    )
                )

                candidates.extend(
                    analysis.get(
                        "objects",
                        []
                    )
                )


                # =============================================
                # CLARIFICATION
                # =============================================

                if ambiguity_result.get(
                    "requires_clarification",
                    False
                ):

                    clarification = (
                        ambiguity_detector
                        .create_clarification_question(
                            candidates
                        )
                    )

                    ambiguity_result[
                        "clarification_question"
                    ] = clarification


                # =============================================
                # RESPONSE VARIABLES
                # =============================================

                final_response = None

                validation_result = None

                decision_result = None


                # =============================================
                # AMBIGUOUS QUESTION
                # =============================================

                if ambiguity_result.get(
                    "requires_clarification",
                    False
                ):

                    final_response = (
                        ambiguity_result.get(
                            "clarification_question",
                            "Could you clarify what you mean?"
                        )
                    )


                    # Semantic validator handles
                    # clarification state.

                    validation_result = (
                        semantic_validator
                        .validate(
                            response=final_response,
                            visual_evidence=analysis,
                            reasoning_result=reasoning_result,
                            ambiguity_result=ambiguity_result
                        )
                    )


                    decision_result = (
                        decision_engine
                        .decide(
                            validation_result=validation_result,
                            response=final_response,
                            clarification=final_response
                        )
                    )


                # =============================================
                # CLEAR QUESTION
                # =============================================

                else:

                    try:

                        with st.spinner(
                            "🤖 Generating evidence-based response..."
                        ):

                            response_generator = (
                                ResponseGenerator()
                            )

                            final_response = (
                                response_generator
                                .generate(
                                    question=question,
                                    visual_evidence=analysis,
                                    reasoning_result=(
                                        reasoning_result
                                    ),
                                    conversation_context=(
                                        context.get(
                                            "previous_messages",
                                            []
                                        )
                                    )
                                )
                            )


                        # =====================================
                        # SEMANTIC VALIDATION
                        # =====================================

                        validation_result = (
                            semantic_validator
                            .validate(
                                response=final_response,
                                visual_evidence=analysis,
                                reasoning_result=reasoning_result,
                                ambiguity_result=ambiguity_result
                            )
                        )


                        # =====================================
                        # FINAL DECISION
                        # =====================================

                        decision_result = (
                            decision_engine
                            .decide(
                                validation_result=(
                                    validation_result
                                ),
                                response=final_response,
                                clarification=(
                                    ambiguity_result.get(
                                        "clarification_question"
                                    )
                                )
                            )
                        )


                    except Exception as e:

                        final_response = (
                            "I was unable to generate "
                            "a reliable answer from "
                            "the available evidence."
                        )


                        validation_result = {
                            "decision": "REJECT",
                            "valid": False,
                            "score": 0.0,
                            "reason": str(e),
                            "evidence_coverage": 0.0,
                            "reference_consistency": 0.0,
                            "uncertainty_score": 0.0,
                            "reasoning_confidence": 0.0,
                            "matched_evidence": []
                        }


                        decision_result = (
                            decision_engine
                            .decide(
                                validation_result=(
                                    validation_result
                                ),
                                response=final_response
                            )
                        )


                # =================================================
                # CONTEXTUAL REASONING
                # =================================================

                st.divider()

                st.subheader(
                    "🧠 Contextual Reasoning"
                )


                st.write(
                    "### Current Question"
                )

                st.write(
                    question
                )


                st.write(
                    "### Context Information"
                )

                st.write(
                    {
                        "has_context":
                            reasoning_result.get(
                                "has_context",
                                False
                            ),

                        "has_reference":
                            reasoning_result.get(
                                "has_reference",
                                False
                            ),

                        "previous_messages":
                            len(
                                context.get(
                                    "previous_messages",
                                    []
                                )
                            )
                    }
                )


                # =================================================
                # REFERENCE
                # =================================================

                st.write(
                    "### Resolved Reference"
                )


                reference = (
                    reasoning_result.get(
                        "resolved_reference"
                    )
                )


                if reference:

                    st.success(
                        f"Reference resolved to: "
                        f"**{reference}**"
                    )

                else:

                    st.warning(
                        "No clear reference could be resolved."
                    )


                # =================================================
                # SUPPORTING EVIDENCE
                # =================================================

                st.write(
                    "### Supporting Evidence"
                )


                evidence = (
                    reasoning_result.get(
                        "supporting_evidence",
                        []
                    )
                )


                if evidence:

                    for item in evidence:

                        st.write(
                            f"- {item}"
                        )

                else:

                    st.write(
                        "No supporting evidence found."
                    )


                # =================================================
                # REASONING STEPS
                # =================================================

                st.write(
                    "### Reasoning"
                )


                for step in (
                    reasoning_result.get(
                        "reasoning",
                        []
                    )
                ):

                    st.write(
                        f"- {step}"
                    )


                # =================================================
                # REASONING CONFIDENCE
                # =================================================

                reasoning_confidence = (
                    reasoning_result.get(
                        "confidence",
                        0.0
                    )
                )


                st.metric(
                    "Reasoning Confidence",
                    f"{reasoning_confidence:.0%}"
                )


                # =================================================
                # FINAL DECISION
                # =================================================

                st.divider()

                st.subheader(
                    "🎯 Final Decision"
                )


                action = (
                    decision_result.get(
                        "action",
                        "REJECT"
                    )
                )


                final_answer = (
                    decision_result.get(
                        "final_response",
                        final_response
                    )
                )


                # -------------------------------------------------
                # ACTION DISPLAY
                # -------------------------------------------------

                if action == "ANSWER":

                    st.success(
                        final_answer
                    )

                elif action == "ANSWER_WITH_CAUTION":

                    st.warning(
                        final_answer
                    )

                elif action == "CLARIFY":

                    st.info(
                        final_answer
                    )

                else:

                    st.error(
                        final_answer
                    )


                # =================================================
                # SEMANTIC EVIDENCE VALIDATION
                # =================================================

                st.write(
                    "### 🛡️ Semantic Evidence Validation"
                )


                if validation_result:

                    col1, col2, col3 = st.columns(3)


                    with col1:

                        st.metric(
                            "Validation Score",
                            f"{validation_result.get('score', 0):.0%}"
                        )


                    with col2:

                        st.metric(
                            "Evidence Coverage",
                            f"{validation_result.get('evidence_coverage', 0):.0%}"
                        )


                    with col3:

                        st.metric(
                            "Reference Consistency",
                            f"{validation_result.get('reference_consistency', 0):.0%}"
                        )


                    st.write(
                        f"**Decision:** "
                        f"`{validation_result.get('decision', 'UNKNOWN')}`"
                    )


                    st.write(
                        validation_result.get(
                            "reason",
                            "No validation reason available."
                        )
                    )


                    matched = (
                        validation_result.get(
                            "matched_evidence",
                            []
                        )
                    )


                    if matched:

                        st.write(
                            "**Evidence supporting the response:**"
                        )


                        for item in matched:

                            st.write(
                                f"- `{item}`"
                            )


                    st.write(
                        "**Reasoning Confidence:** "
                        f"{validation_result.get('reasoning_confidence', 0):.0%}"
                    )


                    st.write(
                        "**Uncertainty Score:** "
                        f"{validation_result.get('uncertainty_score', 0):.0%}"
                    )


                else:

                    st.info(
                        "Semantic validation was not performed."
                    )


                # =================================================
                # FINAL DECISION DETAILS
                # =================================================

                st.write(
                    "### 🎯 Decision Details"
                )


                st.write(
                    f"**Action:** "
                    f"`{decision_result.get('action', 'UNKNOWN')}`"
                )


                st.metric(
                    "Final Decision Confidence",
                    f"{decision_result.get('confidence', 0):.0%}"
                )


                st.write(
                    decision_result.get(
                        "reason",
                        "No decision reason available."
                    )
                )


                # =================================================
                # DEBUG INFORMATION
                # =================================================

                with st.expander(
                    "🔬 View Reasoning Result"
                ):

                    st.json(
                        reasoning_result
                    )


                with st.expander(
                    "🛡️ View Semantic Validation"
                ):

                    st.json(
                        validation_result
                    )


                with st.expander(
                    "🎯 View Final Decision"
                ):

                    st.json(
                        decision_result
                    )


        except Exception as e:

            st.error(
                f"Image analysis failed: {str(e)}"
            )


    # ========================================================
    # CASE 2 — TEXT-ONLY FOLLOW-UP
    # ========================================================

    else:

        question = (
            user_question.strip()
        )


        # =================================================
        # CONTEXT
        # =================================================

        context = (
            context_manager
            .get_relevant_context(
                question
            )
        )


        # =================================================
        # REASONING
        # =================================================

        reasoning_result = (
            reasoning_engine
            .reason(
                question
            )
        )


        # =================================================
        # AMBIGUITY
        # =================================================

        ambiguity_result = (
            ambiguity_detector
            .analyze(
                reasoning_result
            )
        )


        # =================================================
        # PREVIOUS IMAGE EVIDENCE
        # =================================================

        visual_evidence = (
            context.get(
                "latest_image_analysis"
            )
            or {}
        )


        # =================================================
        # CANDIDATES
        # =================================================

        candidates = []

        candidates.extend(
            visual_evidence.get(
                "visible_text",
                []
            )
        )

        candidates.extend(
            visual_evidence.get(
                "objects",
                []
            )
        )


        # =================================================
        # CLARIFICATION
        # =================================================

        if ambiguity_result.get(
            "requires_clarification",
            False
        ):

            clarification = (
                ambiguity_detector
                .create_clarification_question(
                    candidates
                )
            )

            ambiguity_result[
                "clarification_question"
            ] = clarification


        final_response = None

        validation_result = None

        decision_result = None


        # =================================================
        # AMBIGUOUS FOLLOW-UP
        # =================================================

        if ambiguity_result.get(
            "requires_clarification",
            False
        ):

            final_response = (
                ambiguity_result.get(
                    "clarification_question",
                    "Could you clarify what you mean?"
                )
            )


            validation_result = (
                semantic_validator
                .validate(
                    response=final_response,
                    visual_evidence=visual_evidence,
                    reasoning_result=reasoning_result,
                    ambiguity_result=ambiguity_result
                )
            )


            decision_result = (
                decision_engine
                .decide(
                    validation_result=validation_result,
                    response=final_response,
                    clarification=final_response
                )
            )


        # =================================================
        # CLEAR FOLLOW-UP
        # =================================================

        else:

            try:

                with st.spinner(
                    "🤖 Generating evidence-based response..."
                ):

                    response_generator = (
                        ResponseGenerator()
                    )


                    final_response = (
                        response_generator
                        .generate(
                            question=question,

                            visual_evidence=(
                                visual_evidence
                            ),

                            reasoning_result=(
                                reasoning_result
                            ),

                            conversation_context=(
                                context.get(
                                    "previous_messages",
                                    []
                                )
                            )
                        )
                    )


                # =============================================
                # SEMANTIC VALIDATION
                # =============================================

                validation_result = (
                    semantic_validator
                    .validate(
                        response=final_response,
                        visual_evidence=visual_evidence,
                        reasoning_result=reasoning_result,
                        ambiguity_result=ambiguity_result
                    )
                )


                # =============================================
                # FINAL DECISION
                # =============================================

                decision_result = (
                    decision_engine
                    .decide(
                        validation_result=(
                            validation_result
                        ),
                        response=final_response,
                        clarification=(
                            ambiguity_result.get(
                                "clarification_question"
                            )
                        )
                    )
                )


            except Exception as e:

                final_response = (
                    "I was unable to generate "
                    "a reliable answer from the "
                    "available conversation context."
                )


                validation_result = {
                    "decision": "REJECT",
                    "valid": False,
                    "score": 0.0,
                    "reason": str(e),
                    "evidence_coverage": 0.0,
                    "reference_consistency": 0.0,
                    "uncertainty_score": 0.0,
                    "reasoning_confidence": 0.0,
                    "matched_evidence": []
                }


                decision_result = (
                    decision_engine
                    .decide(
                        validation_result=(
                            validation_result
                        ),
                        response=final_response
                    )
                )


        # =================================================
        # REASONING DISPLAY
        # =================================================

        st.subheader(
            "🧠 Contextual Reasoning"
        )


        st.write(
            "### Current Question"
        )

        st.write(
            question
        )


        st.write(
            "### Context Information"
        )

        st.write(
            {
                "has_context":
                    reasoning_result.get(
                        "has_context",
                        False
                    ),

                "has_reference":
                    reasoning_result.get(
                        "has_reference",
                        False
                    ),

                "previous_messages":
                    len(
                        context.get(
                            "previous_messages",
                            []
                        )
                    ),

                "previous_visual_analysis":
                    visual_evidence != {}
            }
        )


        # =================================================
        # RESOLVED REFERENCE
        # =================================================

        st.write(
            "### Resolved Reference"
        )


        reference = (
            reasoning_result.get(
                "resolved_reference"
            )
        )


        if reference:

            st.success(
                f"Reference resolved to: "
                f"**{reference}**"
            )

        else:

            st.warning(
                "No clear reference could be resolved."
            )


        # =================================================
        # SUPPORTING EVIDENCE
        # =================================================

        st.write(
            "### Supporting Evidence"
        )


        evidence = (
            reasoning_result.get(
                "supporting_evidence",
                []
            )
        )


        if evidence:

            for item in evidence:

                st.write(
                    f"- {item}"
                )

        else:

            st.write(
                "No supporting evidence found."
            )


        # =================================================
        # REASONING
        # =================================================

        st.write(
            "### Reasoning"
        )


        for step in (
            reasoning_result.get(
                "reasoning",
                []
            )
        ):

            st.write(
                f"- {step}"
            )


        reasoning_confidence = (
            reasoning_result.get(
                "confidence",
                0.0
            )
        )


        st.metric(
            "Reasoning Confidence",
            f"{reasoning_confidence:.0%}"
        )


        # =================================================
        # FINAL DECISION
        # =================================================

        st.divider()

        st.subheader(
            "🎯 Final Decision"
        )


        action = (
            decision_result.get(
                "action",
                "REJECT"
            )
        )


        final_answer = (
            decision_result.get(
                "final_response",
                final_response
            )
        )


        if action == "ANSWER":

            st.success(
                final_answer
            )

        elif action == "ANSWER_WITH_CAUTION":

            st.warning(
                final_answer
            )

        elif action == "CLARIFY":

            st.info(
                final_answer
            )

        else:

            st.error(
                final_answer
            )


        # =================================================
        # SEMANTIC VALIDATION
        # =================================================

        st.write(
            "### 🛡️ Semantic Evidence Validation"
        )


        if validation_result:

            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Validation Score",
                    f"{validation_result.get('score', 0):.0%}"
                )


            with col2:

                st.metric(
                    "Evidence Coverage",
                    f"{validation_result.get('evidence_coverage', 0):.0%}"
                )


            with col3:

                st.metric(
                    "Reference Consistency",
                    f"{validation_result.get('reference_consistency', 0):.0%}"
                )


            st.write(
                f"**Decision:** "
                f"`{validation_result.get('decision', 'UNKNOWN')}`"
            )


            st.write(
                validation_result.get(
                    "reason",
                    "No validation reason available."
                )
            )


            matched = (
                validation_result.get(
                    "matched_evidence",
                    []
                )
            )


            if matched:

                st.write(
                    "**Evidence supporting the response:**"
                )


                for item in matched:

                    st.write(
                        f"- `{item}`"
                    )


            st.write(
                "**Reasoning Confidence:** "
                f"{validation_result.get('reasoning_confidence', 0):.0%}"
            )


            st.write(
                "**Uncertainty Score:** "
                f"{validation_result.get('uncertainty_score', 0):.0%}"
            )


        else:

            st.info(
                "Semantic validation was not performed."
            )


        # =================================================
        # DECISION DETAILS
        # =================================================

        st.write(
            "### 🎯 Decision Details"
        )


        st.write(
            f"**Action:** "
            f"`{decision_result.get('action', 'UNKNOWN')}`"
        )


        st.metric(
            "Final Decision Confidence",
            f"{decision_result.get('confidence', 0):.0%}"
        )


        st.write(
            decision_result.get(
                "reason",
                "No decision reason available."
            )
        )


        # =================================================
        # DEBUG INFORMATION
        # =================================================

        with st.expander(
            "🔬 View Reasoning Result"
        ):

            st.json(
                reasoning_result
            )


        with st.expander(
            "🛡️ View Semantic Validation"
        ):

            st.json(
                validation_result
            )


        with st.expander(
            "🎯 View Final Decision"
        ):

            st.json(
                decision_result
            )


# ============================================================
# CONVERSATION HISTORY
# ============================================================

if memory.count() > 0:

    st.divider()

    st.subheader(
        "💬 Conversation Memory"
    )


    for message in (
        memory.get_messages()
    ):

        role = message.get(
            "role"
        )


        # =================================================
        # USER
        # =================================================

        if role == "user":

            user_text = (
                message.get(
                    "text"
                )
                or
                "[Image uploaded]"
            )


            st.markdown(
                f"**👤 User:** {user_text}"
            )


            if message.get(
                "image_name"
            ):

                st.caption(
                    f"Image: "
                    f"{message['image_name']}"
                )


        # =================================================
        # ASSISTANT IMAGE ANALYSIS
        # =================================================

        elif role == "assistant":

            analysis = (
                message.get(
                    "image_analysis"
                )
            )


            if analysis:

                st.markdown(
                    "**🤖 Assistant — Visual Analysis**"
                )


                st.caption(
                    "Visual evidence stored in "
                    "conversation memory."
                )


                st.write(
                    "Objects:",
                    analysis.get(
                        "objects",
                        []
                    )
                )


                st.write(
                    "Visible Text:",
                    analysis.get(
                        "visible_text",
                        []
                    )
                )