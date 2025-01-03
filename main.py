import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import logger
from app.routers import items_router, users_router, posts_router

app = FastAPI()

# Выдача изображений на предметы
app.mount("/item_image", StaticFiles(directory="item_image"), name="item_image")

# Выдача изображений на аватарки пользователей
app.mount("/user_image", StaticFiles(directory="user_image"),
          name="user_image")

# Выдача изображений на посты
app.mount("/post_image", StaticFiles(directory="post_image"), name="post_image")

# Выдача изображений компаний
app.mount("/business_image", StaticFiles(directory="business_image"),
          name="business_image")

# Загрузка всех роутеров запросов
app.include_router(items_router, prefix="/items", tags=["Items"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(posts_router, prefix="/posts", tags=["Posts"])

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--test", action="store_true", help="Need test ip (only local hosting")

    args = parser.parse_args()
    startup_ip = "0.0.0.0"
    if args.test:
        startup_ip = "127.0.0.1"
        logger.info("========================")
        logger.info("Start API in local env")
    elif os.name == 'nt':
        logger.critical("=================================")
        logger.critical("Code was stared by Win System. You're crazy, or forget --test flag.")
        logger.critical("=================================")
        exit(2)
    else:
        logger.info("========================")
        logger.info("Start API in VPS")

    uvicorn.run("main:app", host=startup_ip, port=80, reload=True, log_config=f"logs/unicorn_config_log.ini")
