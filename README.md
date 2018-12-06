The Minstrel API
================

Hello there, and welcome to the API behind the minstrel project - connecting performers around the world.




What is Minstrel?
-----------------
Minstrel is an open-source project, with only one goal - to make life easier for performers to get connected to their fans and interested viewers.




Why Minstrel?
-------------
- Minstrel is free. No hidden costs or catches. Maintained and supported purely by fans of performers. 
- Minstrel is interested in **you**. This is a platform specifically made for performers and their fans to share their passion.    
- Minstrel is lightweight. We provide what you need and want, with no additional useless features.




How can I set up my own?
-----------------------
Since Minstrel is free and open-source, everybody is welcome to fork, reuse and make their own version. In this section we will describe what  you need to hit the road running.

- Python
- Pipenv
- MongoDB
- Redis

First make sure python is working on your system, check with
```
python3 -v
```
Configure MongoDB and Redis and then run them

After cloning the repo, simply run:
```
pipenv install
```
When the dependecies are installed, navigate to lib/ and run:
```
pipenv run python3 app.py
```
That should get your own instance of the minstrel API up and running,
from there you can make requests to all routes  defined in app.py with any
web request tool (such as Postman).
