from src.llm_generator import ResearchLLM


class PaperSummarizer:

    def __init__(self):

        print("Initializing paper summarizer...")

        self.llm = ResearchLLM()

        print("Paper summarizer ready.")

    def summarize(self, paper):

        title = paper.get("title", "Unknown")
        text = paper.get("text", "")

        prompt = f"""
Summarize the following computer science research paper.

Paper Title:
{title}

Research Content:
{text}

Create a technically accurate summary using these sections:

1. Research Problem
2. Proposed Approach
3. Key Findings
4. Important Technical Concepts
5. Practical Significance
6. Limitations

Rules:
- Use only information supported by the provided research content.
- Do not invent experiments, results, methods, or conclusions.
- If information is not available, write "Not clearly specified in the provided content."
- Keep the explanation understandable to a computer science student.
"""

        answer = self.llm.generate_answer(
            question="Summarize this research paper.",
            context=prompt
        )

        return answer