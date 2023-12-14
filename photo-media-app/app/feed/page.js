"use client";
import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import ImageCard from "../components/imagecard";
import { useRouter } from "next/navigation";
import Image from "next/image";

import useSessionStorage from "../hooks/useSessionStorage";

const Feed = () => {
  const router = useRouter();

  /*
  const storedUsername = sessionStorage.getItem("username"); // Use sessionStorage to get the username
  const user_id = sessionStorage.getItem("user_id"); // also get userid*/
  //const storedUsername = useSessionStorage("username"); // Use sessionStorage to get the username
  //const user_id = useSessionStorage("user_id");
  //console.log(storedUsername, user_id);

  // If a username is stored in sessionStorage, use that;
  //const username = storedUsername;

  // Various State variables
  const [userList, setUsers] = useState([]);
  const [userFolloweesList, setUserFolloweesList] = useState([]);
  const [fullUserList, setFullUsers] = useState({});
  const [feedList, setFeed] = useState([{}]);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [imageData, setImageData] = useState(null);
  const [showUploadButton, setShowUploadButton] = useState(false);
  const [caption, setCaption] = useState("");
  const [img, setImg] = useState(null);

  const [storedUsername, setStoredUsername] = useState([]);
  const [user_id, setUser_id] = useState([]);

  useEffect(() => {
    setStoredUsername(sessionStorage.getItem("username")); //useSessionStorage("username"));
    setUser_id(sessionStorage.getItem("user_id")); //useSessionStorage("user_id"));
  }, []); //empty dependency array

  // Executes immediately after the first render to get the list of users
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch(
          "https://fk3tsbpl03.execute-api.us-east-2.amazonaws.com/prod/users"
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Process the data to grab only the username
        let names = [];
        for (let i = 0; i < data.length; i++) {
          names.push(data[i][1]);
        }

        // Set the names
        setUsers(names);

        let userObjs = {};
        for (let i = 0; i < data.length; i++) {
          userObjs[data[i][1]] = data[i][0];
        }
        // Set the full user list
        setFullUsers(userObjs);
      } catch (error) {
        console.log(error);
        //alert("Error: Could not get users!");
      }
    };

    const fetchFeed = async () => {
      try {
        const response = await fetch(
          "https://fk3tsbpl03.execute-api.us-east-2.amazonaws.com/prod/feed/" +
            user_id
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Process the data to grab each image
        let feed = [];
        for (let i = 0; i < data.length; i++) {
          feed.push({
            username: data[i][1],
            url: data[i][2],
            caption: data[i][3],
          });
        }

        // Set the feed
        setFeed(feed);
      } catch (error) {
        console.log(error);
        //alert("Error: Could not get feed!");
      }
    };

    //for use by initial get and refresh
    const fetchFollowees = async () => {
      try {
        const response = await fetch(
          "https://fk3tsbpl03.execute-api.us-east-2.amazonaws.com/prod/users/followees/" +
            user_id
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Process the data to grab only the username
        let names = [];
        for (let i = 0; i < data.length; i++) {
          names.push(data[i]);
        }

        // Set the names
        setUserFolloweesList(names);
      } catch (error) {
        console.log(error);
        //alert("Error: Could not get users!");
      }
    };

    fetchUsers();
    fetchFollowees();
    fetchFeed();
  }, [storedUsername, user_id]); // Empty dependency array ensures the effect runs once on component mount

  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setUploadedImage(reader.result); // Set the uploaded image for preview
        const base64String = reader.result.split(",")[1]; // Extract base64 data
        setImageData(base64String);
        setShowUploadButton(true); // Show the upload button when an image is uploaded
      };
      reader.readAsDataURL(file);
    }
  };

  const handleImageUpload = async () => {
    try {
      const response = await fetch(
        "https://fk3tsbpl03.execute-api.us-east-2.amazonaws.com/prod/post/" +
          user_id,
        {
          method: "POST",
          body: JSON.stringify({
            filename: caption + ".jpg",
            data: imageData,
            caption: caption,
          }),
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      alert("Image uploaded successfully!");
      // You can add further logic or handle the response as needed
    } catch (error) {
      console.error("Error uploading image:", error);
    }
  };

  const handleFollow = (user) => {
    // Handle the follow user logic
    let followee_id = fullUserList[user];

    const followUser = async () => {
      try {
        const response = await fetch(
          "https://fk3tsbpl03.execute-api.us-east-2.amazonaws.com/prod/users/follow?" +
            "follower=" +
            user_id +
            "&followee=" +
            followee_id,
          {
            method: "PUT",
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        window.location.reload();
        //alert("User followed successfully!");

        //update followees list
        fetchFollowees();
        fetchFeed();
        // You can add further logic or handle the response as needed
      } catch (error) {
        console.error("Error following user:", error);
        //alert("Error: Could not follow user!");
      }
    };

    followUser();
  };

  const handleUnfollow = (user) => {
    // Handle the follow user logic
    let followee_id = fullUserList[user];

    const unfollowUser = async () => {
      try {
        const response = await fetch(
          "https://fk3tsbpl03.execute-api.us-east-2.amazonaws.com/prod/users/unfollow?" +
            "follower=" +
            user_id +
            "&followee=" +
            followee_id,
          {
            method: "DELETE",
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        window.location.reload();
        //alert("User unfollowed successfully!");
        fetchFollowees();
        fetchFeed();
        // You can add further logic or handle the response as needed
      } catch (error) {
        console.error("Error unfollowing user:", error);
        //alert("Error: Could not unfollow user! ");
      }
    };

    unfollowUser();
  };

  const handleRefreshFeed = () => {
    // Implement the logic to refresh the feed
    console.log("Refreshing feed...");

    // Just refresh the page
    window.location.reload();
    //router.refresh();
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-900 via-slate-950-opacity-70 to-black text-white items-center overflow-auto space-y-4">
      {/* Three sections (left middle right) */}
      <div className="flex justify-between w-full mt-6 px-8">
        {/* Left Section - Photo Upload */}
        <div className="w-1/4 flex flex-col items-center">
          <h1 className="text-3xl font-medium text-center">Upload a Photo</h1>
          <input
            type="file"
            accept="image/jpeg"
            onChange={handleUpload}
            className="p-2 pr-4 border-2 border-blue-500 text-white rounded-md cursor-pointer mt-4"
          />
          {uploadedImage && (
            <Image
              src={uploadedImage}
              alt="Uploaded"
              className="mt-2 rounded-md"
              style={{ maxWidth: "200px" }}
            />
          )}
          {showUploadButton && (
            <div className="mt-2">
              <input
                type="text"
                value={caption}
                onChange={(e) => setCaption(e.target.value)}
                placeholder="Enter caption"
                className="p-2 border border-gray-300 rounded-md text-blue-500"
              />
              <button
                onClick={handleImageUpload}
                className="px-4 py-2 bg-blue-500 text-white hover:bg-blue-600 rounded-lg ml-2"
              >
                Upload Image
              </button>
            </div>
          )}
        </div>

        {/* Center Section */}
        <div className="items-center w-1/3 flex flex-col">
          <h1 className="text-3xl font-medium">
            {/* Welcome to your Feed, {username} */}
            Welcome to your Feed, {storedUsername}
          </h1>
          <button
            onClick={handleRefreshFeed}
            className="hover:bg-gray-500 border-2 border-white text-white p-2 rounded-md cursor-pointer mt-4"
          >
            Refresh Feed
          </button>
          <div className="mt-4 items-center justify-center">
            {feedList.map((item, index) => (
              <div key={index} className="mt-4">
                <ImageCard
                  src={
                    "https://photo-media-app-jackebs.s3.us-east-2.amazonaws.com/" +
                    item.url
                  }
                  alt={`Image ${index + 1}`}
                  user={item.username}
                  caption={`${item.caption || "No Caption"}`}
                  textColor="white"
                />
              </div>
            ))}
          </div>
        </div>

        {/* Right Section - Follow Users */}
        <div className="w-1/3 flex flex-col items-center">
          <h2 className="text-3xl font-semibold mb-2 text-center">
            Following:
          </h2>
          <table className="table-auto mt-3">
            <thead>
              <tr>
                <th className="border px-4 py-2">User</th>
                <th className="border px-4 py-2">Action</th>
              </tr>
            </thead>
            <tbody>
              {userFolloweesList.map((user, idx) => (
                <tr key={idx} className="mb-2">
                  <td className="border px-4 py-2">{user}</td>
                  <td className="border px-4 py-2">
                    <button
                      onClick={() => handleUnfollow(user)}
                      className="hover:bg-emerald-400 bg-opacity-30 text-white px-2 py-1 rounded-md cursor-pointer"
                    >
                      Unfollow
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <h2 className="text-3xl font-semibold mb-2 mt-5 text-center">
            Follow Users
          </h2>
          <table className="table-auto mt-3">
            <thead>
              <tr>
                <th className="border px-4 py-2">User</th>
                <th className="border px-4 py-2">Action</th>
              </tr>
            </thead>
            <tbody>
              {userList
                .filter(
                  (user) =>
                    !userFolloweesList.includes(user) && user !== storedUsername
                ) // Exclude users in the "Following" list and the current user
                .map((user) => (
                  <tr key={user} className="mb-2">
                    <td className="border px-4 py-2">{user}</td>
                    <td className="border px-4 py-2">
                      <button
                        onClick={() => handleFollow(user)}
                        className="hover:bg-emerald-400 bg-opacity-30 text-white px-2 py-1 rounded-md cursor-pointer"
                      >
                        Follow
                      </button>
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Feed;
