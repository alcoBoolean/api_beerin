from typing import Optional

from fastapi import APIRouter, Query, Header

from app import db, logger

router = APIRouter()


@router.get("")
async def get_items():
    """
    Получить список предметов. Лимит в 10 за запрос.
    :return:
    """
    return db.fetch_items()


@router.get("/")
async def get_item(item_id: int):
    """
    Получение предметов по его ID
    :param item_id:
    :return:
    """
    res = db.fetch_item_by_id(int(item_id))
    return res


@router.get("/filter")
async def filter_items(
        country: Optional[str] = Query(None),
        style: Optional[str] = Query(None),
        types: Optional[str] = Query(None),
        alcohol_range: Optional[str] = Query(None),  # Ожидаем диапазон в виде строки "2-4"
        density_range: Optional[str] = Query(None),  # То же для плотности
):
    """
    Получение списка "отфильрованных" предметов. Лимит на 10 за запрос.
    :param country:
    :param style:
    :param types:
    :param alcohol_range:
    :param density_range:
    :return:
    """

    # TODO сделать докрутку информации (после 0-10, выдавать 11-20, 21-30 и тд.
    def parse_range(range_str):
        """
        Парсим промежуток. Получаем мин-макс.
        :param range_str: Обязательно int"-"int
        :return:
        """
        if range_str:
            try:
                lower, upper = map(float, range_str.split("-"))
                return lower, upper
            except ValueError:
                return None
        return None

    # Собираем фильтры в словарь
    filters = {
        "country": country,
        "style": style,
        "color": types,
        "alcohol_percentage": parse_range(alcohol_range),
        "density": parse_range(density_range)
    }

    # Получаем данные
    items = db.get_items_by_filter(filters)
    return items


@router.get("/reviews")
async def get_item_reviews(item_id: int = Header(..., alias="item_id")):
    """
    Получить отзывы на конкретный предмет по ID
    :param item_id:
    :return:
    """
    try:
        answer = db.get_reviews_by_item(item_id)
        return answer
    except Exception as ex:
        logger.error(ex)
        raise ex
