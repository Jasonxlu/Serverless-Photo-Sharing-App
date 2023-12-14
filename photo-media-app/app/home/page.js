// Home.js
"use client";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import ImageCard from "../components/imagecard";
import Title from "../components/title";
import { useRef } from "react";

import { useRouter } from "next/navigation";

import Image1 from "../assets/image1.jpg";
import Image2 from "../assets/image2.jpg";
import Image3 from "../assets/image3.jpg";
import Image4 from "../assets/image4.jpg";

export default function Home() {
  const [username, setUsername] = useState("");
  //const navigate = useNavigate();

  const router = useRouter();

  const scrollTargetRef = useRef(null);

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  // Send the username to the API to get added to the database
  const handleRegister = async () => {
    // No Empty usernames
    if (!username) {
      alert("Error: Username cannot be empty!");
      return;
    }

    // Call API to add the username to the database
    try {
      const response = await fetch(
        "https://fk3tsbpl03.execute-api.us-east-2.amazonaws.com/prod/users/add/" +
          username,
        {
          method: "PUT",
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      response.json().then((data) => {
        sessionStorage.setItem("user_id", data.userid[0]);
        console.log(data.userid[0]);
      });

      // Store the username in sessionStorage
      sessionStorage.setItem("username", username);

      // Redirect to the "feed" page with the username as a query parameter
      //navigate(`/feed?username=${encodeURIComponent(username)}`);
      router.push(`/feed?username=${encodeURIComponent(username)}`)
    } catch (error) {
      alert("Error: Username already exists!");
    }
  };

  const handleLogin = async () => {
    // No Empty usernames
    if (!username) {
      alert("Error: Username cannot be empty!");
      return;
    }

    try {
      const response = await fetch(
        "https://fk3tsbpl03.execute-api.us-east-2.amazonaws.com/prod/users/" +
          username,
        {
          method: "GET",
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      response.json().then((data) => {
        sessionStorage.setItem("user_id", data);
        console.log(data);
      });

      // Store the username in sessionStorage
      sessionStorage.setItem("username", username);

      //console.log("setting username", username);
      
      // Redirect to the "feed" page with the username as a query parameter
      //navigate(`/feed?username=${encodeURIComponent(username)}`);
      router.push(`/feed?username=${encodeURIComponent(username)}`);
    } catch (error) {
      alert("Error: User does not exist!");
    }
  };

  return (
    <div>
      <Title scrollTargetRef={scrollTargetRef} />
      <div
        ref={scrollTargetRef}
        className="flex flex-col items-center min-h-screen py-8"
      >
        <h1 className="text-6xl font-bold mt-10">Share your Mid Moments!</h1>
        <p className="text-xl mt-3">Get started below with your username.</p>

        <div className="flex items-center justify-center w-0">
          {/* Input for Username */}
          <input
            type="text"
            value={username}
            onChange={handleUsernameChange}
            placeholder="Enter your username"
            className="mt-4 p-2 border border-gray-300 rounded-md text-blue-500"
          />

          {/* Button to Get Started */}
          <button
            onClick={handleRegister}
            className="mt-4 px-6 py-2 ml-2 bg-blue-500 text-white hover:bg-blue-600 rounded-lg"
          >
            Register
          </button>

          {/* Button to Get Started */}
          <button
            onClick={handleLogin}
            className="mt-4 px-6 py-2 ml-2 bg-yellow-500 text-white hover:bg-yellow-600 rounded-lg"
          >
            Login
          </button>
        </div>

        {/* Image Cards */}
        <div className="flex flex-row mt-8 space-x-8">
          <ImageCard
            src={Image1}
            alt="Image 1"
            user="M1d_Momenter"
            caption="Mid Moment, we ballin"
          />
          <ImageCard
            src={Image2}
            alt="Image 2"
            user="Television-lover31"
            caption="*Static*"
          />
          <ImageCard
            src={Image3}
            alt="Image 3"
            user="EggsAreFriendsNotFood"
            caption="Me and my friends!"
          />
          <ImageCard
            src={Image4}
            alt="Image 4"
            user="Plant-Mom"
            caption="This cactus bit me."
          />
        </div>
      </div>
    </div>
  );
}
