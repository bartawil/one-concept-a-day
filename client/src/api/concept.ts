export async function getConceptByCategory(category: string): Promise<{ concept: string }> {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/get-concept?category=${encodeURIComponent(category)}`);
    if (!response.ok) {
        throw new Error("Failed to fetch concept");
    }
    return await response.json();
}
