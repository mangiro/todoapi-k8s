from sqlalchemy import MetaData, create_engine


engine = create_engine(
    "sqlite:///./tasks.db",
    # required for sqlite
    connect_args={"check_same_thread": False},
)

metadata = MetaData()
