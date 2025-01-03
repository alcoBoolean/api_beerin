import datetime

from fastapi import Header, APIRouter

from app import db

router = APIRouter()


@router.get("")
async def get_list_of_posts():
    """
    Получить список всех постов. Лимит 10 за запрос
    :return:
    """
    # TODO сделать докрутку информации (после 0-10, выдавать 11-20, 21-30 и тд.
    answer = db.get_list_of_posts()
    return answer


@router.post("/like_post")
async def reg_new_like_post(login: str = Header(...), password: str = Header(...),
                            post_id: int = Header(..., alias="post_id")):
    """
    Поставить или снять лайк `посту`. Требуется авторизация
    :param login:
    :param password:
    :param post_id:
    :return:
    """
    # TODO реализовать проверку на формат данных

    try:
        print(login, password, int(post_id))
        answer = db.add_post_like(login, password, int(post_id))
        return answer
    except Exception as ex:
        print(ex)

    return {"error": "Invalid headers", "time": datetime.datetime.now()}


@router.get("/get_comments")
async def get_comments_from_post(post_id: int = Header(..., alias="post_id")):
    """
    Получить список комментариев от поста. Лимит 10 за запрос
    :param post_id:
    :return:
    """
    # TODO реализовать проверку на формат данных
    # TODO сделать докрутку информации (после 0-10, выдавать 11-20, 21-30 и тд.

    try:
        print(post_id)
        answer = db.get_comments_from_post(int(post_id))
        return answer
    except Exception as ex:
        print(ex)
