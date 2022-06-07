# FastAPI-JWT-auth-feed-app (Hosted on GCP : [Link](http://34.70.209.181:8000/docs))

- Backend for feed application that allows JWT Authenticated users to create, post and view feed/status/tweet.
- Data is stored and accessed from mongoDB atlas cluster hosted on AWS.
- Used FastAPI for creating API endpoints.

## Demo Video
Link to demo video : https://youtu.be/KRYPuZnvHvM
## Functionalities 
- User authentication with JSON Web tokens (JWT)
- Users have to register.
- Users have to login to view and create posts / get access to protected routes.
- Protected routes have been set up and can be accessed by authenticated users to view all posts, search & view post by id, view posts by a particular author
- Data is stored and accessed from mongoDB atlas cluster hosted on AWS

### Setup
- Fork and clone the repository 
- cd into the root folder `fastAPI-JWT-auth-feed-app`
- Run the below commands
```
pip install -r requirements.txt
```
- Create .env file in root directory, add the following to it
```
MONGODB_URI = YOUR_MONGO_DB_ATLAS_URI
```
- Make sure you mongoDB atlas cluster has database named fastapiJWT with users and posts collections as shown below
![image](https://user-images.githubusercontent.com/65719940/152414463-fc4d79e9-64f6-4bac-9a55-0f5069748f9d.png)

- Or Contact me for my mongoDB credentials for testing purposes : sandur43@gmail.com
- From the root directory, run the below command and open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view the SWAGGER UI of the API routes.
```
uvicorn src.main:app --reload
```
- Authenticate yourself and test the application APIs.

## Screenshots
### FastAPI routes
![image](https://user-images.githubusercontent.com/65719940/152411339-19db25d2-38db-4d1c-83e8-5c65b4693fba.png)

### User details stored in MongoDB atlas cluster
![image](https://user-images.githubusercontent.com/65719940/152411969-19cfd413-fd92-41fa-bac1-3d46f1245edb.png)

### Posts/Feed details stored in MongoDB atlas cluster
![image](https://user-images.githubusercontent.com/65719940/152412108-de6ec525-0f49-4a51-824e-800f8de062d3.png)

