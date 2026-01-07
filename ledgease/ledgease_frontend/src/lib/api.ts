const ACCESS_KEY = "Access-Key";
const REFRESH_KEY = "Refresh-Key";

// WILL HAVE TO USE HttpsOnly COOKIES LATER FOR TOKENS
// JUST USING AS BOILERPLATE TESTING FOR NOW

export function getAccessToken(): string | null {
    return localStorage.getItem(ACCESS_KEY);
}   

export function setToken(token: string, refresh?: string) {
    localStorage.setItem(REFRESH_KEY, token);
    if (refresh) {
        localStorage.setItem(ACCESS_KEY, refresh);
    }
}

export function clearTokens() {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
}

export async function apiFetch<T>(
    path: string, // relative path to API endpoint
    options: RequestInit = {} // default to empty object
): Promise<T> {
    const accessToken = getAccessToken(); // Gets Access token from localStorage
    const headers = new Headers(options.headers); // Create headers object
    headers.set('Content-Type', 'application/json'); // Set content type

    if (accessToken) {
        headers.set('Authorization', `Bearer ${accessToken}`); // Set auth header if token exists
    } //Allows request.user to be identified by backend and thus isAuthenticated

    const response = await fetch(path, {...options, headers}); 
    const contentType = response.headers.get('Content-Type');
    const isJson = contentType?.includes('application/json');
    const data = isJson ? await response.json() : await response.text();

    console.log('API Response:', data);
    console.log('Status Code:', response.status);
    
    if (!response.ok) {
        throw data;
    }
    return data as T;
}