from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


class ResearchLLM:

    def __init__(self):
        print("Loading Qwen LLM...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            dtype=torch.float32
        )

        self.model.eval()

        print("Qwen LLM loaded successfully")

    def generate_answer(
        self,
        question,
        context,
        conversation_history=None
    ):

        history_text = ""

        if conversation_history:

            for item in conversation_history:

                history_text += (
                    f"User: {item['question']}\n"
                    f"Assistant: {item['answer']}\n"
                )

        prompt = f"""
You are an academic Computer Science research assistant.

You MUST answer the user's question using ONLY the information
contained in the RESEARCH CONTEXT.

STRICT RULES:

1. Do not use outside knowledge.
2. Do not invent facts, findings, methods, results, or technologies.
3. Do not assume information that is not explicitly supported by the
   research context.
4. If the context does not contain enough information to answer the
   question, say:

   "The available research context does not provide enough information
   to answer this question reliably."

5. Do not add technologies or concepts that are not mentioned in the
   retrieved research context.
6. When explaining a technical concept, connect the explanation to the
   retrieved research papers.
7. Prefer concise and factual answers.
8. When possible, mention the relevant paper title and arXiv paper ID.
9. Never claim that a paper reported a result unless that result appears
   in the provided context.
10. Previous conversation may be used only to understand the question.
    It must NOT be treated as research evidence.

PREVIOUS CONVERSATION:
{history_text}

RESEARCH CONTEXT:
{context}

USER QUESTION:
{question}

Before answering, internally check:

- Is the answer supported by the research context?
- Am I introducing information that is not present?
- Am I confusing different architectures or methods?
- If evidence is insufficient, should I state that clearly?

Now provide a clear, accurate, evidence-based answer.
"""

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a strict, evidence-based Computer Science "
                    "research assistant. Never invent information."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt"
        )

        with torch.no_grad():

            outputs = self.model.generate(
                **inputs,
                max_new_tokens=300,

                # Deterministic generation
                do_sample=False,

                # Prevent excessive repetition
                repetition_penalty=1.1
            )

        generated_tokens = outputs[
            0
        ][
            inputs["input_ids"].shape[1]:
        ]

        answer = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        return answer.strip()