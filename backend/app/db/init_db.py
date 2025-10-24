from app.db.session import Base, engine
import app.models.fund as fund_model
import app.models.transaction as tx_model
import app.models.document as doc_model

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

if __name__ == "__main__":
    init_db()
