from the_classifier.pipeline import Pipeline
from the_classifier.extractor import Extractor
import json

pipe = Pipeline()
values = pipe.start(
    "../TheCrawler/tmp/TheCralwer.Spiders.Immobiliare_2021_01_06_19_38_57_551037.json"
)
extractor = Extractor("./results/result")
extractor.extract_clusters(values)
