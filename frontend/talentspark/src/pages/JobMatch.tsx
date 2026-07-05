import { useState } from "react";
import { matchJobs, embedJobs, semanticSearch } from "../Services/RagService";
import type { JobMatchResult, SemanticSearchResult } from "../types/rag";

function JobMatch() {
    const [skills, setSkills] = useState("");
    const [experience, setExperience] = useState("");
    const [matches, setMatches] = useState<JobMatchResult[]>([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [searchResults, setSearchResults] = useState<SemanticSearchResult[]>([]);
    const [loading, setLoading] = useState(false);
    const [embedMsg, setEmbedMsg] = useState("");

    const handleEmbed = async () => {
        setLoading(true);
        setEmbedMsg("");
        try {
            const result = await embedJobs();
            setEmbedMsg(result.message);
        } catch {
            setEmbedMsg("Failed to embed jobs. Is Qdrant running?");
        } finally {
            setLoading(false);
        }
    };

    const handleMatch = async () => {
        if (!skills.trim()) return;
        setLoading(true);
        setMatches([]);
        try {
            const result = await matchJobs(skills, experience);
            setMatches(result.matches);
        } catch {
            setMatches([]);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async () => {
        if (!searchQuery.trim()) return;
        setLoading(true);
        setSearchResults([]);
        try {
            const result = await semanticSearch(searchQuery);
            setSearchResults(result.results);
        } catch {
            setSearchResults([]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: "20px", maxWidth: "800px", margin: "0 auto", textAlign: "left" }}>
            <h2>Smart Job Match</h2>

            <div style={{ marginBottom: "20px", padding: "15px", border: "1px solid #ccc", borderRadius: "5px" }}>
                <h3>Step 1: Embed Jobs into Vector DB</h3>
                <p style={{ fontSize: "14px", marginBottom: "10px" }}>Click below to embed all jobs from the database into Qdrant for semantic search.</p>
                <button onClick={handleEmbed} disabled={loading} style={{ padding: "8px 20px" }}>
                    {loading ? "Embedding..." : "Embed All Jobs"}
                </button>
                {embedMsg && <p style={{ marginTop: "10px", color: "green" }}>{embedMsg}</p>}
            </div>

            <div style={{ marginBottom: "20px", padding: "15px", border: "1px solid #ccc", borderRadius: "5px" }}>
                <h3>Step 2: Semantic Job Search</h3>
                <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search jobs... e.g. 'python backend developer'"
                    style={{ width: "70%", padding: "8px", marginRight: "10px" }}
                />
                <button onClick={handleSearch} disabled={loading || !searchQuery.trim()} style={{ padding: "8px 20px" }}>
                    Search
                </button>
                {searchResults.length > 0 && (
                    <div style={{ marginTop: "10px" }}>
                        {searchResults.map((r, i) => (
                            <div key={i} style={{ padding: "10px", borderBottom: "1px solid #eee" }}>
                                <strong>{r.title}</strong> — Score: {r.score}
                                <p>{r.description}</p>
                                <small>Salary: {r.salary}</small>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <div style={{ padding: "15px", border: "1px solid #ccc", borderRadius: "5px" }}>
                <h3>Step 3: Match Your Profile</h3>
                <input
                    type="text"
                    value={skills}
                    onChange={(e) => setSkills(e.target.value)}
                    placeholder="Your skills... e.g. 'Python, React, SQL'"
                    style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
                />
                <input
                    type="text"
                    value={experience}
                    onChange={(e) => setExperience(e.target.value)}
                    placeholder="Your experience... e.g. '3 years in web development'"
                    style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
                />
                <button onClick={handleMatch} disabled={loading || !skills.trim()} style={{ padding: "8px 20px" }}>
                    {loading ? "Matching..." : "Find Matching Jobs"}
                </button>
                {matches.length > 0 && (
                    <div style={{ marginTop: "10px" }}>
                        <h4>Top Matches</h4>
                        {matches.map((m, i) => (
                            <div key={i} style={{ padding: "10px", borderBottom: "1px solid #eee" }}>
                                <strong>{m.title}</strong> — Match: {m.match_score}%
                                <p>{m.description}</p>
                                <small>Salary: {m.salary}</small>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

export default JobMatch;
