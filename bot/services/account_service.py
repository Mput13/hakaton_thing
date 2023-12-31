from bot.repositories.user_repository import user_repository


class AccountService:
    """
    Взаимодействие с профилем пользователя и его настройками
    """

    async def register_account(self, session, data):
        user = await user_repository.create_user(session, data)
        return user


account_service = AccountService()  # в случае с нормальным DI, этот объект бы создавался через него в отдельном месте, а не тут
