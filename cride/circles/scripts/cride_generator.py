import random
import csv
from ..models import Circle, Membership
from ...users.models import User, Profile
from ...rides.models import Ride


def run():
    with open("circles.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)[1:]
        for row in rows:
            c = Circle.objects.create(
                name=row[0],
                slug_name=row[1],
                is_public=row[2] == '1',
                is_verified=row[3] == '1',
                is_limited=row[4] != '0',
                members_limit=0 if row[4] == '0' else int(row[4])
            )
            print(c)

run()

n_users = 60
users = []
for _ in range(n_users):
    user = User.objects.create(
        email='dummyuser{}@gmail.com'.format(_),
        first_name='Dummy {}'.format(_),
        last_name='User {}'.format(_),
        username='uniquerusername00{}'.format(_),
        password='vanderpapi'
    )
    Profile.objects.create(user=user)
    users.append(user)
    print("New user create", user.email)


circles = Circle.objects.all()

for circle in circles:
    for user in users:
        m = Membership.objects.create(
            user=user,
            profile=user.profile,
            circle=circle,
            remaining_invitations=10
        )
        print("New member added", m)


for circle in circles:
    for offerer in random.choices(users, k=random.randint(1, 10)):
        available_seats = random.randint(1, 8)

        ride = Ride.objects.create(
            offered_by=offerer,
            offered_in=circle,
            available_seats=available_seats,
            departure_location='Departure location',
            arrival_location='Arrival location',
        )
        passengers = random.choices(users, k=random.randint(1, available_seats))
        passengers = [u for u in passengers if u != offerer]
        ride.passengers.add(*passengers)
        ride.save()
        print("New ride created", ride)