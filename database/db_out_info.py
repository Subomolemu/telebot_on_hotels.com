from . import main_db


def out(user_id):
    with main_db.db:
        for i in main_db.Info.select().order_by(main_db.Info.user_id):
            if i.user_id == str(user_id):
                yield f'{i.command_time}, "{i.command}", \nCписок найденных отелей: {i.hotels}'
