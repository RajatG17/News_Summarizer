from google.adk.agents import LlmAgent

class SummarizerAgent(LlmAgent):
    """
    Summarizer: Summarizes fetched items into 2-3 sentences each.
    """
    def __init__(self, llm, name="summarizer", max_length=400):
        super().__init__(name=name, llm=llm)
        self.max_length = max_length

    def summarize(self, items):
        """
        :param items: A dict of items
        :return: A list of summary strings. Each
        """

        summaries = []
        for item in items:
            prompt = f"Can you please summarize the following news item into 3-4 sentences:\nTitle: {item['title']}\nDescription: {item['description']}"
            response = self.llm.predict(prompt, max_tokens=self.max_length)
            summaries.append(response)

        return summaries
