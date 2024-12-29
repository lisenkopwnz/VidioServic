def user_status_subscription(user):
    """Функция возвращает статус подписки клиента,
        если подпика активна возвращает True ,в противном случае False"""
    if hasattr(user, 'profile') and user.profile:
        return user.profile.subscription_active
    else:
        # Если профиля нет, нужно вернуть False
        return False
