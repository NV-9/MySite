cd myauth/
del /s /q migrations
cd ../main/
del /s /q migrations
cd ../tutor/
del /s /q migrations
cd ..
python manage.py makemigrations myauth
python manage.py makemigrations main 
python manage.py makemigrations tutor 
python manage.py migrate 
python manage.py loaddata data/profiles.json
python manage.py loaddata data/courses.json
python manage.py runserver