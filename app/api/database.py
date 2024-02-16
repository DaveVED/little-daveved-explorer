from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Create an engine that manages connections to the database.
# The `connect_args` argument is specifically for SQLite. It disables same thread check to allow multiple threads to use the same connection.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session factory bound to this engine. This allows us to create sessions which are the working copy of the database.
# `autocommit=False` ensures that changes are not committed automatically, giving you control over transactions.
# `autoflush=False` prevents the session from flushing changes to the database every time a query is executed.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for declarative class definitions. 
# Any model you define will inherit from this class to gain directives to describe the database table they represent.
Base = declarative_base()
