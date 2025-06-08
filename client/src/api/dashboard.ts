export async function getDailyConcept(userId: string, category: string): Promise<{ term: string; explanation: string }> {
    const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/daily-concept?category=${encodeURIComponent(category)}&user_id=${userId}`
    );
    if (!response.ok) {
        throw new Error("Failed to fetch concept");
    }
    return await response.json();
}



export async function addUserInterest(userId: string, interest: string) {
    const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/user/${userId}/interests/add`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(interest),
        }
    );
    if (!response.ok) throw new Error("Failed to add interest");
}

export async function removeUserInterest(userId: string, interest: string) {
    const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/user/${userId}/interests/remove`,
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(interest),
        }
    );
    if (!response.ok) throw new Error("Failed to remove interest");
}
