
from sqlalchemy import and_, or_, cast, Date
from time import perf_counter

from database import SessionLocal
import models 

me = 3
max_distance = 1000000
start_date = "2023-10-01"
end_date = "2023-11-01"


t1 = perf_counter()
try:
    db = SessionLocal()
    results = db.query(models.Exposure, models.Person, models.Location).filter(
        and_(
            or_(
                and_(models.Exposure.person_a == me, models.Exposure.person_b == models.Person.id, models.Exposure.location_a == models.Location.id),
                and_(models.Exposure.person_b == me, models.Exposure.person_a == models.Person.id, models.Exposure.location_b == models.Location.id)),
            models.Exposure.date_exposed >= cast(start_date, Date),
            models.Exposure.date_exposed <= cast(end_date, Date),
            models.Exposure.min_distance < max_distance,
            
        )).all()

    for (exposure, the_other_person_i_met, my_location_where_we_met) in results:
        print(exposure.id, the_other_person_i_met.first_name, my_location_where_we_met.id)
finally:
    db.close()

t2 = perf_counter()
print(t2-t1)