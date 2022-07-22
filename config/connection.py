from config.database import SessionLocal, engine, Base

class Connection:
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
            engine.dispose()
            db.bind.dispose()