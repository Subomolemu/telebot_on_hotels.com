from . import main_db


def add(user_id, command_date, command, hotels):
    hotels = '\n- ' + '\n- '.join(hotels)
    main_db.Info.create(user_id=user_id, command_time=command_date, command=command, hotels=hotels)
