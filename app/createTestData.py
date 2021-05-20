from app import db
from app.models import User, ChoreList, ChoreProgress, ChoreAssignments


#  add users

# brice = User(username='Brice', email='brice@hotmail.com', password_hash='brice', user_type='Parent')
# brice.set_password(brice.password_hash)
# db.session.add(brice)
# db.session.commit()

hadley = User(username='Hadley', email='hadley@hotmail.com', password_hash='hadley', user_type='Child')
hadley.set_password(hadley.password_hash)
db.session.add(hadley)
db.session.commit()

