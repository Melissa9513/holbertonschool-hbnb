from app import create_app, db
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)