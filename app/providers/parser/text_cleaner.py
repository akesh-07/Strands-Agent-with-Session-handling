import re

class TextCleaner:
    @staticmethod
    def clean(text: str) -> str:
        """
        Cleans unnecessary whitespace and normalizes text.
        """
        # Remove multiple newlines
        text = re.sub(r'\n+', '\n', text)
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        return text.strip()
