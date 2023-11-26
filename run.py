
from app import  db
from app.models import User

u = User(username='susan', email='susan@example.com')
u.set_password('cat')
db.session.add(u)
db.session.commit()


# from app import app, db
# from app.models import User, Post

# # app.app_context().push()
# # u = User(username='bob', email='bob@bob.com')
# # db.session.add(u)
# # db.session.commit()
# # users = User.query.all()
# # for u in users:
# #     print(u.id, u.username)
# app.app_context().push()
# u = User.query.get(2)
# p = Post(body='my first post!', author=u)
# db.session.add(p)
# db.session.commit()