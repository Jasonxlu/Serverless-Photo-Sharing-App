/** @type {import('next').NextConfig} */
const nextConfig = {};

module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "photo-media-app-jackebs.s3.us-east-2.amazonaws.com",
        port: "",
      },
    ],
  },
};
