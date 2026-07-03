import api from "./api";
import type { ChatResponse } from "../types/chat";

export async function askChat(message: string): Promise<string> {
    const response = await api.post<ChatResponse>("/chat/ask", { message });
    return response.data.response;
}

export async function askCareerChat(message: string, session_id: string): Promise<string> {
    const response = await api.post<ChatResponse>("/chat/ask_career", { message, session_id });
    return response.data.response;
}
