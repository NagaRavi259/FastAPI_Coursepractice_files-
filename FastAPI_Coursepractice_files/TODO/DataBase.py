from sqlalchemy import create_engine # We imported Create_engine to create a data base connecting
                                     # engine between python to sqlitebd
from sqlalchemy.orm import sessionmaker # We imported a session maker to create a 
                                        # session between Sqlitedb and python
from sqlalchemy.ext.declarative import declarative_base


SQLalchemy_DataBase_url = "sqlite:///./todos.db" # Created Sqlitedb url
engine = create_engine(SQLalchemy_DataBase_url,connect_args={"check_same_thread":False}) 
# Started a sqlitedb engine between python andsqlitedb

sessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)
## Created a seeion
base = declarative_base()

"""
sqlite> .mode table
sqlite> select * from todos;
+----+-----------------+----------------------+----------+----------+
| id |      title      |     description      | priority | complete |
+----+-----------------+----------------------+----------+----------+
| 1  | go to the store | Pickup eggss         | 5        | 0        |
| 2  | cut the lawn    | Grass getting long   | 3        | 0        |
| 3  | Feed the dog    | He is getting hungry | 5        | 0        |
+----+-----------------+----------------------+----------+----------+

sqlite> .mode markdown       
sqlite> select * from todos;
| id |      title      |     description      | priority | complete |
|----|-----------------|----------------------|----------|----------|
| 1  | go to the store | Pickup eggss         | 5        | 0        |
| 2  | cut the lawn    | Grass getting long   | 3        | 0        |
| 3  | Feed the dog    | He is getting hungry | 5        | 0        |

sqlite> .mode box
sqlite> select * from todos;
┌────┬─────────────────┬──────────────────────┬──────────┬──────────┐
│ id │      title      │     description      │ priority │ complete │
├────┼─────────────────┼──────────────────────┼──────────┼──────────┤
│ 1  │ go to the store │ Pickup eggss         │ 5        │ 0        │
│ 2  │ cut the lawn    │ Grass getting long   │ 3        │ 0        │
│ 3  │ Feed the dog    │ He is getting hungry │ 5        │ 0        │
└────┴─────────────────┴──────────────────────┴──────────┴──────────┘


"""