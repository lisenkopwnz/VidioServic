import logging
import random
import string



def slug_generation(size_slug: int) -> str:
    """ Функция используется для генерации слага """
    all_symbols = string.ascii_uppercase + string.digits
    slug = "".join(random.choice(all_symbols) for _ in range(size_slug))
    return slug


def user_status_subscription(user):
    """Функция возвращает статус подписки клиента,
        если подпика активна возвращает True ,в противном случае False"""
    return user.profile.subscription_active
