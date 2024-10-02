from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql://postgres:Dhanu123#@localhost:5432/Test_db'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

{
  "route": {
    "total_distance": 80215,
    "total_time": 1201,
    "total_load": 424,
    "vehicle_routes": [
      {
        "vehicle_id": 0,
        "no_of_orders_for_route": 6,
        "total_weight_for_route": 68,
        "total_distance_for_route": 17673,
        "total_time_for_route": 264,
        "orders": [
          {
            "id": 0,
            "order_id": 1,
            "order_weight": 0,
            "latitude": 11.519855,
            "longitude": 104.934508,
            "arrive_time": "11:15AM - 11:15AM"
          },
          {
            "id": 1,
            "order_id": 2,
            "order_weight": 12,
            "latitude": 11.552482,
            "longitude": 104.933399,
            "arrive_time": "11:26AM - 11:26AM"
          },
          {
            "id": 13,
            "order_id": 14,
            "order_weight": 5,
            "latitude": 11.555217,
            "longitude": 104.926641,
            "arrive_time": "11:36AM - 11:36AM"
          },
          {
            "id": 12,
            "order_id": 13,
            "order_weight": 28,
            "latitude": 11.555217,
            "longitude": 104.926641,
            "arrive_time": "11:41AM - 11:41AM"
          },
          {
            "id": 7,
            "order_id": 8,
            "order_weight": 3,
            "latitude": 11.555217,
            "longitude": 104.926641,
            "arrive_time": "11:46AM - 11:46AM"
          },
          {
            "id": 18,
            "order_id": 19,
            "order_weight": 20,
            "latitude": 11.570927,
            "longitude": 104.918242,
            "arrive_time": "11:59AM - 11:59AM"
          }
        ]
      },
      {
        "vehicle_id": 1,
        "no_of_orders_for_route": 9,
        "total_weight_for_route": 151,
        "total_distance_for_route": 30076,
        "total_time_for_route": 312,
        "orders": [
          {
            "id": 0,
            "order_id": 1,
            "order_weight": 0,
            "latitude": 11.519855,
            "longitude": 104.934508,
            "arrive_time": "11:15AM - 11:15AM"
          },
          {
            "id": 21,
            "order_id": 22,
            "order_weight": 27,
            "latitude": 11.557692,
            "longitude": 104.930453,
            "arrive_time": "11:26AM - 11:26AM"
          },
          {
            "id": 14,
            "order_id": 15,
            "order_weight": 15,
            "latitude": 11.560042,
            "longitude": 104.929001,
            "arrive_time": "11:32AM - 11:32AM"
          },
          {
            "id": 24,
            "order_id": 25,
            "order_weight": 17,
            "latitude": 11.560042,
            "longitude": 104.929001,
            "arrive_time": "11:37AM - 11:37AM"
          },
          {
            "id": 16,
            "order_id": 17,
            "order_weight": 23,
            "latitude": 11.590121,
            "longitude": 104.8989,
            "arrive_time": "11:57AM - 11:57AM"
          },
          {
            "id": 17,
            "order_id": 18,
            "order_weight": 30,
            "latitude": 11.591938,
            "longitude": 104.899099,
            "arrive_time": "12:03PM - 12:03PM"
          },
          {
            "id": 10,
            "order_id": 11,
            "order_weight": 10,
            "latitude": 11.595234,
            "longitude": 104.899892,
            "arrive_time": "12:15PM - 12:15PM"
          },
          {
            "id": 22,
            "order_id": 23,
            "order_weight": 18,
            "latitude": 11.575012,
            "longitude": 104.915002,
            "arrive_time": "12:32PM - 12:32PM"
          },
          {
            "id": 23,
            "order_id": 24,
            "order_weight": 11,
            "latitude": 11.570421,
            "longitude": 104.915122,
            "arrive_time": "12:40PM - 12:40PM"
          }
        ]
      },
      {
        "vehicle_id": 2,
        "no_of_orders_for_route": 12,
        "total_weight_for_route": 205,
        "total_distance_for_route": 32466,
        "total_time_for_route": 625,
        "orders": [
          {
            "id": 0,
            "order_id": 1,
            "order_weight": 0,
            "latitude": 11.519855,
            "longitude": 104.934508,
            "arrive_time": "3:53PM - 3:53PM"
          },
          {
            "id": 3,
            "order_id": 4,
            "order_weight": 28,
            "latitude": 11.550041,
            "longitude": 104.934402,
            "arrive_time": "4:07PM - 4:07PM"
          },
          {
            "id": 6,
            "order_id": 7,
            "order_weight": 25,
            "latitude": 11.548522,
            "longitude": 104.931116,
            "arrive_time": "4:19PM - 4:19PM"
          },
          {
            "id": 2,
            "order_id": 3,
            "order_weight": 7,
            "latitude": 11.544872,
            "longitude": 104.928413,
            "arrive_time": "4:31PM - 4:31PM"
          },
          {
            "id": 5,
            "order_id": 6,
            "order_weight": 1,
            "latitude": 11.589118,
            "longitude": 104.897911,
            "arrive_time": "5:00PM - 5:00PM"
          },
          {
            "id": 15,
            "order_id": 16,
            "order_weight": 17,
            "latitude": 11.590821,
            "longitude": 104.89871,
            "arrive_time": "5:07PM - 5:07PM"
          },
          {
            "id": 8,
            "order_id": 9,
            "order_weight": 25,
            "latitude": 11.594891,
            "longitude": 104.900748,
            "arrive_time": "5:14PM - 5:14PM"
          },
          {
            "id": 11,
            "order_id": 12,
            "order_weight": 26,
            "latitude": 11.573832,
            "longitude": 104.913492,
            "arrive_time": "5:33PM - 5:33PM"
          },
          {
            "id": 20,
            "order_id": 21,
            "order_weight": 24,
            "latitude": 11.571527,
            "longitude": 104.916321,
            "arrive_time": "5:39PM - 5:39PM"
          },
          {
            "id": 19,
            "order_id": 20,
            "order_weight": 30,
            "latitude": 11.570818,
            "longitude": 104.91589,
            "arrive_time": "5:44PM - 5:44PM"
          },
          {
            "id": 4,
            "order_id": 5,
            "order_weight": 5,
            "latitude": 11.573182,
            "longitude": 104.923245,
            "arrive_time": "5:51PM - 5:51PM"
          },
          {
            "id": 9,
            "order_id": 10,
            "order_weight": 17,
            "latitude": 11.571922,
            "longitude": 104.921837,
            "arrive_time": "5:58PM - 5:58PM"
          }
        ]
      }
    ]
  }
}

