Hello!

If you are reading this, you have found the GitHub repo for our team project in Intro to Software Engineering!
Feel free to make a clone of this repo!

Instructions for starting the docker containers for both servers:
```
# If running on a virtual container (like AWS Academy),
# edit the ALLOWED_HOSTS in cs3300team7/job_connect/job_connect/settings.py

# From the root directory of the repo "cs3300team7"
sudo docker compose build
sudo docker compose up

# Once both containers are running, connect to the instance at http://localhost:8000
# or at your public IP port 8000
```
