from peewee import SqliteDatabase, Model, CharField


db = SqliteDatabase('history.db')


class BaseModel(Model):

    class Meta:
        database = db


class Info(BaseModel):
    user_id = CharField()
    command = CharField()
    command_time = CharField()
    hotels = CharField()


with db:
    db.create_tables([Info])
