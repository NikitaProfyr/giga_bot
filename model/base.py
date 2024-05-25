"""
Регистрация моделей для миграций.
Импортируй свои классы моделей(таблицы) сюда, прежде чем начать миграции
"""
from model.model_settings import Base
from .user_models import User
