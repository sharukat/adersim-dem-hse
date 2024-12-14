import re
import logging
import pandas as pd
from typing import List
from tqdm.notebook import tqdm_notebook
from transformers import AutoTokenizer
from deepmultilingualpunctuation import PunctuationModel


def extract_youtube_video_id(url):
    pattern = r"v=([a-zA-Z0-9_-]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


def preprocess_text(text):
    try:
        if text is not None:
            filler = ["um", "uh", "hmm", "mhm", "uh-huh", "ah", "huh", "hm"]
            pattern = r'\b(?:' + '|'.join(re.escape(f) for f in filler)+r')\b'
            cleaned_text = re.sub(pattern, '', text, flags=re.IGNORECASE)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

            pattern = (
                r'\['
                r'(Music|Musique|Música|Musica|Musik|Applause|'
                r'Applaudissements|Aplausos|Applausi|\xa0__\xa0)'
                r'\]'
            )
            cleaned_text = re.sub(pattern, '', cleaned_text)
            cleaned_text = cleaned_text.replace("\n", " ")
            return cleaned_text
    except Exception:
        logging.error("An error occurred", exc_info=True)
        return "Not available"


def fix_punctuations(text):
    model = PunctuationModel()
    try:
        text = model.restore_punctuation(text)
        return text
    except Exception:
        logging.error("An error occurred", exc_info=True)
        return text


def remove_emojis(text):
    try:
        if text is not None:
            # Define emoji pattern
            emoji_pattern = re.compile(
                "["
                "\U0001F600-\U0001F64F"  # Faces
                "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
                "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
                "\U0001F700-\U0001F77F"  # Alchemical Symbols
                "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                "\U0001FA00-\U0001FA6F"  # Chess Symbols
                "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                "\U00002702-\U000027B0"  # Dingbats
                "\U000024C2-\U0001F251"  # Enclosed characters
                "]+",
                flags=re.UNICODE
            )
            # Remove emojis
            return emoji_pattern.sub(r'', text)
    except Exception:
        logging.error("An error occurred", exc_info=True)
        return "Not available"


def count_tokens(dataframe: pd.DataFrame) -> List[int]:
    tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen2.5-32B-Instruct',
                                              trust_remote_code=True)
    lengths = []
    for row in tqdm_notebook(dataframe.itertuples(index=True),
                             total=dataframe.shape[0]):
        tokens = tokenizer.encode(row.page_content)
        lengths.append(len(tokens))
    return lengths
