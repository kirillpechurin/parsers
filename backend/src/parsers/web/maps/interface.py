from abc import ABCMeta, abstractmethod


class MapReviewsInterface:

    @abstractmethod
    def get_reviews(self):
        raise NotImplementedError

    @abstractmethod
    def find(self):
        raise NotImplementedError

    @abstractmethod
    def transition_to_reviews(self):
        raise NotImplementedError
