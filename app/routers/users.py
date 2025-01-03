import datetime

from fastapi import Header, APIRouter

from app import db
from error import AuthenticationError

router = APIRouter()


@router.post("/registration")
async def registration_new_user(login: str = Header(...), password: str = Header(...),
                                phone_number: str = Header(..., alias="phone_number"),
                                name: str = Header(...), surname: str = Header(...)):
    """
    Регистрация нового пользователя
    :param login:
    :param password:
    :param phone_number:
    :param name:
    :param surname:
    :return:
    """
    # TODO реализовать проверку на формат данных

    print(login, password, phone_number)
    answer = db.register_user(login, password, phone_number, name, surname)
    return answer


@router.get("/auth")
async def get_user_auth_info(login: str = Header(...), password: str = Header(...)):
    """
    Функция проверят валидность данных пользователя для авторизации

    TODO: должен выдавать токен авторизации
    :param login:
    :param password:
    :return:
    """
    try:
        return db.check_auth_user(login, password)
    except AuthenticationError as ex:
        return ex.as_dict()


@router.get("/likes")
async def get_list_of_favorites(login: str = Header(...), password: str = Header(...)):
    """
    Получить список избранных `предметов` от юзера. Требуется авторизация.
    :param login:
    :param password:
    :return:
    """
    # TODO реализовать проверку на формат данных

    print(login, password)
    answer = db.get_list_of_favorites(login, password)
    return answer


@router.post("/like_item")
async def reg_new_like_item(login: str = Header(...), password: str = Header(...),
                            item_id: int = Header(..., alias="item_id")):
    """
    Поставить или снять лайк `предмету`. Требуется авторизация
    :param login:
    :param password:
    :param item_id:
    :return:
    """
    # TODO реализовать проверку на формат данных

    print(login, password, int(item_id))
    answer = db.add_favourites(login, password, int(item_id))
    return answer


@router.get("/friends")
async def get_list_of_friends(login: str = Header(...), password: str = Header(...)):
    """
    Получить список всех друзей пользователя. Требуется авторизация.
    :param login:
    :param password:
    :return:
    """
    # TODO реализовать проверку на формат данных

    answer = db.get_user_friend_list(login, password)
    return answer


@router.get("/friend_info")
async def get_friend_info(login: str = Header(...), password: str = Header(...),
                          friend_id: int = Header(..., alias="friend_id")):
    """
    Получить информацию о конкретном друге. Требуется авторизация, требуется наличие "друга" в друзьях пользователя
    :param login:
    :param password:
    :param friend_id:
    :return:
    """
    # TODO реализовать проверку на формат данных
    try:
        answer = db.get_user_friend_info(login, password, friend_id)
        return answer
    except ValueError as ex:
        return {"error": "Friend_id is int value.", "time": datetime.datetime.now()}  # TODO вынести в метод


@router.get("/friend_info/favorites")
async def get_list_of_favorites_by_friend(login: str = Header(...), password: str = Header(...),
                                          friend_id: int = Header(..., alias="friend_id")):
    """
    Получить список избранного от своего друга. Требуется авторизация и наличие "друга" в списке друзей пользователя.
    :param login:
    :param password:
    :param friend_id:
    :return:
    """

    try:
        answer = db.get_favorites_by_friend(login, password, int(friend_id))
        return answer
    except ValueError as ex:
        return {"error": "Friend_id is int value.", "time": datetime.datetime.now()}  # TODO вынести в метод


@router.delete("")
async def delete_user(login: str = Header(...), password: str = Header(...)):
    """
    Удаление юзера. Требуется авторизация.
    :param login:
    :param password:
    :return:
    """
    # todo сделать это админ фичёй

    return db.delete_user(login, password)
