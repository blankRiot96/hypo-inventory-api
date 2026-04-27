from sqlmodel import Session, SQLModel, create_engine

sqlite_url = "sqlite:///memory"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

SQLModel.metadata.create_all(engine)


def get_test_session():
    with Session(engine) as session:
        return session
