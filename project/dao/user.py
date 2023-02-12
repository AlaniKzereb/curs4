from project.dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, user_id):
        return self.session.query(User).get(user_id)

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_id):
        ent = User(**user_id)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, user_id):
        user = self.get_one(user_id)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_id):
        user = self.get_one(user_id.get("id"))
        user.name = self.get_one(user_id.get("name"))
        user.password = self.get_one(user_id.get("password"))
        user.role = self.get_one(user_id.get("role"))

        self.session.add(user)
        self.session.commit()

    def get_user_by_email(self, email):
        user = self.session.query(User).filter(User.email == email).one_or_none()
        return user
