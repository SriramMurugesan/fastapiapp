# Architecture
backend/
  app/
    --main.py
    --database.py
    models/
    --users.py
    --company.py
    --job.py
    schemas/
    --users.py
    --company.py
    --job.py
    routers/
    --users.py
    --company.py
    --job.py
    utils/
    --token.py
    --security.py
    --oauth2.py
    --
  alembic.ini
  alembic/env.py


# Task 
1.push to github
2.try run application ./env/Scripts/activate --> uvicorn app.main:app --reload
3.dont blindly trusting on Ai
4.read the error look for our file name dont care of other files errors like library files errors
5.if files doesnt have error if its like unprocessible identifier or dependency error then ask ai to fix it
6.ask ai to suggest changes not to correct-----
register->login->create compnay->create job
have two variants -> role1:admin
role2:candidate-->try test all apis with both roles