export const env = {
  appName: process.env.NEXT_PUBLIC_APP_NAME || "Generic Swarm Ops",
  appEnv: process.env.NEXT_PUBLIC_APP_ENV || "development",
  apiBaseUrl: process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000/api/v1",
  enableRegistration: process.env.NEXT_PUBLIC_ENABLE_REGISTRATION !== "false",
  enableBilling: process.env.NEXT_PUBLIC_ENABLE_BILLING !== "false",
  enableSso: process.env.NEXT_PUBLIC_ENABLE_SSO === "true",
  // Opt-in only: real backend is the default product path (recommend, special-skills, etc.).
  demoMode: process.env.NEXT_PUBLIC_DEMO_MODE === "true",
};
