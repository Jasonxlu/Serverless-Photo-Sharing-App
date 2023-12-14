"use client";
import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./home/page";
import Feed from "./feed/page";
import exp from "constants";

const App = () => {
  return <Home />/*(
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/feed" element={<Feed />} />
      </Routes>
    </Router>
  );*/
};

export default App;
