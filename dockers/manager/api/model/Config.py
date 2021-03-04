from app import db


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Colum(db.String(), unique=True, nullable=False)
    value = db.Colum(db.String())


    def __repr__(self):
        return f"<Config {self.key}={self.value}>"