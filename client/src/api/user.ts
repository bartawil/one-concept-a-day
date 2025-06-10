// client/src/api/user.ts
export interface UserCreate {
  username: string;
  email: string;
  password: string;  // Now required on frontend too
  interests: string[];
}

export interface UserResponse {
  id: string;
  username: string;
  email: string;
  interests: string[];
}
  
export async function createUser(user: UserCreate): Promise<UserResponse> {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/users`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    const errorMessage = errorData?.detail || "Failed to create user";
    throw new Error(errorMessage);
  }

  return await response.json();
}

export async function loginUser(credentials: {
  email: string;
  password: string;
}): Promise<UserResponse> {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      // Handle specific HTTP status codes for better error messages
      if (response.status === 401) {
        throw new Error("Invalid email or password");
      } else if (response.status === 429) {
        throw new Error("Too many login attempts");
      } else if (response.status >= 500) {
        throw new Error("Server error. Please try again later");
      } else {
        const errorData = await response.json().catch(() => null);
        const errorMessage = errorData?.detail || "Login failed";
        throw new Error(errorMessage);
      }
    }

    return await response.json();
  } catch (error) {
    // Handle network errors specifically
    if (error instanceof TypeError && error.message.includes("fetch")) {
      throw new Error("Network error. Please check your connection");
    }
    // Re-throw other errors as-is
    throw error;
  }
}


