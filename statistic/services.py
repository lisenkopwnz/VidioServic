import os


class SignificanceRating:

    w_likes: float = float(os.getenv('W_LIKES', 1))
    w_dislikes: float = float(os.getenv('W_DISLIKES', -1))
    w_comments: float = float(os.getenv('W_COMMENTS', 0.5))
    w_views: float = float(os.getenv('W_VIEWS', 0.1))
    w_votes: float = float(os.getenv('W_VOTES', 1))

    def __init__(self,
                 number_of_likes,
                 number_of_dislikes,
                 number_of_comments,
                 number_of_views):

        self.number_of_likes: int = number_of_likes
        self.number_of_dislikes: int = number_of_dislikes
        self.number_of_comments: int = number_of_comments
        self.number_of_views: int = number_of_views


    def validate_positive_counts(self)-> bool:
        """ Проверка на положительное значение атрибутов экземпляра """
        if all(x > 0 for x in
           [self.number_of_likes, self.number_of_dislikes, self.number_of_comments, self.number_of_views]):
            return True
        return False


    def calculate(self)-> float:
        """ Считаем рейтинг видео """
        match self.validate_positive_counts():
            case False:
                return 0.0
            case True:
                numerator: float = ((self.number_of_likes * self.w_likes) +
                                    (self.number_of_dislikes * self.w_dislikes) +
                                    (self.number_of_comments * self.w_comments) +
                                    (self.number_of_views * self.w_views))

                denominator: float = float(self.number_of_likes +
                                           self.number_of_dislikes +
                                           self.number_of_comments +
                                           self.number_of_views +
                                           self.w_votes)

                if denominator == 0:
                    return 0.0

                return round(numerator/denominator,4)

    def reset(self, likes, dislikes, comments, views) -> None:
        """ Присваиваем актуальные атрибуты экземпляру """
        self.number_of_likes = likes
        self.number_of_dislikes = dislikes
        self.number_of_comments = comments
        self.number_of_views = views
