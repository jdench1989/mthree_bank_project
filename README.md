### Intro
This project combines a flask web API and a MySQL database into a basic simulated banking app. Particular attention has been paid to implementing sessions and user login. Additionally constraints and triggers are used in the MySQL database in order to ensure that CRUD operations are performed in a logical way. 

Docker is used to containerise the application to simplify ongoing deployment. Separate containers are created for the database and the server. The database is automatically configured and populated with dummy data at creation.

An Entity Relationship Diagram for the database can be found in the main repo directory. 

### Setup
1. Download, install and run Docker desktop - https://www.docker.com/products/docker-desktop/
2. Clone this repo to your machine
   

### Building and running your application

When you're ready, navigate to the cloned repo on your machine and start the application by running:
`docker compose up --build`.

When the container has finished building and is running properly you will see:
![image](https://github.com/user-attachments/assets/0ec3a81e-287c-467b-b43f-c94b6adb9003)


The application will be available at http://localhost:5000.

