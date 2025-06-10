// Helper function to get auth token from localStorage
function getAuthToken(): string | null {
    const user = localStorage.getItem("user");
    if (!user) return null;
    const userData = JSON.parse(user);
    return userData.access_token || null;
}

// Helper function to get auth headers
function getAuthHeaders(): HeadersInit {
    const token = getAuthToken();
    const headers: HeadersInit = {
        "Content-Type": "application/json"
    };
    
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }
    
    return headers;
}

export async function getDailyConcept(userId: string, category: string): Promise<{ term: string; explanation: string }> {
    const token = getAuthToken();
    if (!token) {
        throw new Error("No authentication token found");
    }

    const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/daily-concept?category=${encodeURIComponent(category)}&user_id=${userId}`,
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );
    
    if (!response.ok) {
        if (response.status === 401) {
            throw new Error("Authentication expired");
        } else if (response.status === 403) {
            throw new Error("Access denied");
        }
        throw new Error("Failed to fetch concept");
    }
    return await response.json();
}



export async function addUserInterest(userId: string, interest: string) {
    const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/user/${userId}/interests/add`,
        {
            method: "POST",
            headers: getAuthHeaders(),
            body: JSON.stringify(interest),
        }
    );
    if (!response.ok) {
        if (response.status === 401) {
            throw new Error("Authentication expired");
        } else if (response.status === 403) {
            throw new Error("Access denied");
        }
        throw new Error("Failed to add interest");
    }
}

export async function removeUserInterest(userId: string, interest: string) {
    const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/user/${userId}/interests/remove`,
        {
            method: "POST",
            headers: getAuthHeaders(),
            body: JSON.stringify(interest),
        }
    );
    if (!response.ok) {
        if (response.status === 401) {
            throw new Error("Authentication expired");
        } else if (response.status === 403) {
            throw new Error("Access denied");
        }
        throw new Error("Failed to remove interest");
    }
}
