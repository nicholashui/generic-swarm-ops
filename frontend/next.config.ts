import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow HMR when the browser hits 127.0.0.1 while the server prints localhost (or vice versa).
  allowedDevOrigins: ["127.0.0.1", "localhost"],
};

export default nextConfig;
