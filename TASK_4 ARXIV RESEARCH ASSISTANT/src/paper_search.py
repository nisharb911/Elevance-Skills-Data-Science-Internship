from src.retriever import ResearchRetriever


class PaperSearcher:

    def __init__(self):

        print("Initializing paper search...")

        self.retriever = ResearchRetriever()

        print("Paper search ready.")

    def search(self, query, top_k=10):

        results = self.retriever.search(
            query=query,
            top_k=top_k
        )

        return results