from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL database connection URL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/messaging_system"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()