from the_classifier.classifier import Classifier
from the_classifier.cleaner import Cleaner
from the_classifier.loader import Loader
class Pipeline(object):
    def __init__(self):
        self.pipe = [
            Loader(),
            Cleaner(),
            Classifier()
        ]

    def start(self, args):
        value = args
        for element in self.pipe:
            value = element.process(value)
        return value
