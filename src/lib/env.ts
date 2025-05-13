interface EnvVariables {
  JWT_SECRET: string;
  // Add other required env vars here
}

// Validate and export environment variables
export const env: EnvVariables = {
  JWT_SECRET: import.meta.env.VITE_JWT_SECRET || '',
  // Initialize other env vars
};

// Validate required environment variables
const requiredVars: Array<keyof EnvVariables> = ['JWT_SECRET'];
for (const key of requiredVars) {
  if (!env[key]) {
    console.error(`Missing required environment variable: ${key}`);
  }
}
