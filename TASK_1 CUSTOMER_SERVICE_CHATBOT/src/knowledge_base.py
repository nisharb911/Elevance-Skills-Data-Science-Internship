from pathlib import Path


# ---------------------------------------------------------
# Find the project root directory
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------
# Knowledge base file
# ---------------------------------------------------------

KNOWLEDGE_FILE = BASE_DIR / "knowledge" / "company_faq.txt"


# ---------------------------------------------------------
# Load knowledge base
# ---------------------------------------------------------

def load_knowledge_base() -> str:
    """
    Load the company FAQ knowledge base.

    Returns
    -------
    str
        Complete knowledge base content.
    """

    if not KNOWLEDGE_FILE.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KNOWLEDGE_FILE}"
        )

    return KNOWLEDGE_FILE.read_text(
        encoding="utf-8"
    )


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":

    knowledge = load_knowledge_base()

    print("Knowledge base loaded successfully.")
    print(f"Characters: {len(knowledge)}")

