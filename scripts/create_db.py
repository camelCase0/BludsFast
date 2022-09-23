from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import DATABASE_URL


def main():
    engine = create_engine(DATABASE_URL)
    session = Session(bind=engine.connect())

    session.execute("""create table users(
        id integer not null primary key,
        email varchar(256),
        password varchar(256),
        name varchar(256),
        blood_type varchar(256),
        status varchar(256),
        created_at varchar(256)
        );""")

    session.execute("""create table donations(
        record_id integer not null primary key,
        user_id integer references users,
        volume integer,
        date varchar(256)
        );""")

    session.execute("""create table receives(
        record_id integer not null primary key,
        user_id integer references users,
        volume integer
        );""")

    session.close()


if __name__ == '__main__':
    main()