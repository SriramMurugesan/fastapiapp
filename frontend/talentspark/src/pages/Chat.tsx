import { useState } from "react";
import { askCareerChat } from "../Services/ChatService";
import type { ChatMessage } from "../types/chat";

function Chat() {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [sessionId] = useState(() => "session_" + Date.now());

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage: ChatMessage = { role: "user", content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput("");
        setLoading(true);

        try {
            const response = await askCareerChat(input, sessionId);
            const botMessage: ChatMessage = { role: "bot", content: response };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error("Chat error:", error);
            const errorMessage: ChatMessage = { role: "bot", content: "Error: Could not get response" };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page-container" style={{ marginTop: '2rem' }}>
            <h2>Career Chat</h2>
            <div className="card" style={{ display: 'flex', flexDirection: 'column', height: '60vh' }}>
                <div style={{ flex: 1, overflowY: "auto", padding: "1rem", display: 'flex', flexDirection: 'column' }}>
                    {messages.length === 0 && (
                        <div style={{ margin: 'auto', color: 'var(--text)', textAlign: 'center' }}>
                            <p style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>Ask me anything about your career!</p>
                            <p style={{ opacity: 0.7 }}>Powered by Llama 3.3</p>
                        </div>
                    )}
                    {messages.map((msg, i) => (
                        <div key={i} className={`chat-message ${msg.role === "user" ? "chat-user" : "chat-bot"}`}>
                            <strong style={{ display: 'block', marginBottom: '0.25rem', opacity: 0.8, fontSize: '0.85rem' }}>
                                {msg.role === "user" ? "You" : "Bot"}
                            </strong>
                            <p style={{ margin: 0 }}>{msg.content}</p>
                        </div>
                    ))}
                    {loading && (
                        <div className="chat-message chat-bot" style={{ opacity: 0.7 }}>
                            <em>Thinking...</em>
                        </div>
                    )}
                </div>
                <form onSubmit={handleSend} style={{ margin: 0, maxWidth: '100%', padding: '1rem', borderTop: '1px solid var(--border)', display: 'flex', gap: '1rem', boxShadow: 'none' }}>
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your message..."
                        style={{ marginBottom: 0, flex: 1 }}
                        disabled={loading}
                    />
                    <button type="submit" disabled={loading || !input.trim()}>Send</button>
                </form>
            </div>
        </div>
    );
}

export default Chat;
