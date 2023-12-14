CREATE DATABASE photoshare;

USE photoshare;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS followers;
DROP TABLE IF EXISTS posts;

CREATE TABLE users
(
userid			int not null AUTO_INCREMENT,
username 		varchar(64) not null,
PRIMARY KEY 	(userid),
UNIQUE 			(username)
);
ALTER TABLE users AUTO_INCREMENT = 80001;

CREATE TABLE followers
(
followid		int not null AUTO_INCREMENT,
followerid		int not null,
followeeid		int not null,
PRIMARY KEY		(followid),
FOREIGN KEY		(followerid) REFERENCES users(userid),
FOREIGN KEY		(followeeid) REFERENCES users(userid)
);
ALTER TABLE followers AUTO_INCREMENT = 2001;

CREATE TABLE posts
(
postid			int not null AUTO_INCREMENT,
posterid		int not null, -- userid of poster
bucketkey		varchar(128) not null, -- location of image in bucket
tmstmp			varchar(64) not null DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- timestamp generated when row inserted
caption 		varchar(256),
PRIMARY KEY		(postid),
FOREIGN KEY		(posterid) REFERENCES users(userid),
UNIQUE			(bucketkey)
);
ALTER TABLE posts AUTO_INCREMENT = 1001

