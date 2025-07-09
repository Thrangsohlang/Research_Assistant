import yake
from keybert import KeyBERT

# text
text = "Velvet bean–Mucuna pruriens var. utilis, also known as mucuna—is a twining annual leguminous vine common to most parts of the tropics. Its growth is restricted to the wet-season as it dies at the onset of the cold season. It has large trifoliate leaves (i.e. has three leaflets) and very long vigorous twining stems that can extend over two–three metres depending on growth conditions. When planted at the beginning of the growing season, flowers normally form at the end of March/early April. These flowers are deep purple and appear underneath the foliage. Seeds are large, ovoid shaped (±10 mm long) and of different colours, ranging from white, grey, brown to black and mottled."

# Yake extractor
# kw_extractor = yake.KeywordExtractor()
# keywords = kw_extractor.extract_keywords(text)

# KeyBert Extractor
kw_model = KeyBERT()
keywords = kw_model.extract_keywords(text)

for kw, score in keywords:
    print(f"{kw}: {score}")