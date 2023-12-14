# Overview
This application is a simple photo-sharing social media app that allows users to post images with captions and view posts made by other users. They can choose to create a new account or log into an existing one without authentication. From there, the user can choose to follow or unfollow other users. This determines which posts show up in their feed, which includes their own posts and the posts of the users they follow in order from most to least recent.

# Architecture 
The project consists of a Next.js frontend client hosted on Vercel and connected to the backend via AWS API Gateway. A serverless implementation is used with several lambda functions to access and modify data stored in RDS and images stored in S3. This general architecture is pictured below:


# Database
The database contains 3 tables which store the following information:
- Users
  - Stores each user with a unique user ID and a unique username that they provide.
- Followers
  - Stores all of the follower-followee relationships between users
- Posts
  - Stores all posts, including the user ID of the poster, the location at which the image is stored in S3, the caption for the image, and the time at which the post was made.

# Object Store
The S3 bucket stores all of the images posted by the users. A given user’s images are stored in a folder with their username (since usernames are unique), and each image is assigned a UUID when uploaded to the folder.

# API
The lambda functions are doing all the heavy lifting computation-wise and are accessible to the client via AWS API Gateway.

| API Endpoint| HTTP Method | Query Params | Action | Lambda Function|
| ----------- | ----------- | ---------- | ---------- | ---------- |
| /users      | GET | None | Return all users’ user IDs and usernames | get_users           |
| /users/add/{uname}   | PUT |  None  | Create a new user with username uname | add_user |
| /users/follow   | PUT | follower, followee | Create new relationship where follower follows followee           |  follow          |
| /users/unfollow   | PUT | follower, followee | Remove relationship where follower follows followee            |    unfollow        |
| /users/followees/{follower}| GET| None | Return all the user ids of the users follower follows            |      get_followees      |
| /feed/{userid}   | GET | None | Return the posts (image bucket keys, captions, and user ids of posters) made by userid and all users they follow            |  get_feed          |
| /post/{userid}   | POST | None | Create a new post by userid with the image and caption included in the request body             |  post_image          |
