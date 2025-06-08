// client/src/api/user.ts
export interface UserCreate {
  username: string;
  email: string;
  interests: string[];
}
  
export async function createUser(user: UserCreate) {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/users/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  });

  if (!response.ok) {
    throw new Error("Failed to create user");
  }

  return await response.json();
}

export async function loginUser(credentials: {
  email: string;
  password: string;
}) {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    throw new Error("Login failed");
  }

  return await response.json();
}


  