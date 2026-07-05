import { useState } from "react";
import { analyseResume } from "../Services/RagService";

function ResumeAnalyser() {
    const [resumeText, setResumeText] = useState("");
    const [analysis, setAnalysis] = useState("");
    const [loading, setLoading] = useState(false);

    const handleAnalyse = async () => {
        if (!resumeText.trim()) return;
        setLoading(true);
        setAnalysis("");
        try {
            const result = await analyseResume(resumeText);
            setAnalysis(result.analysis);
        } catch {
            setAnalysis("Failed to analyse resume. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page-container" style={{ marginTop: '2rem' }}>
            <h2>Resume Analyser</h2>
            <div className="card">
                <textarea
                    value={resumeText}
                    onChange={(e) => setResumeText(e.target.value)}
                    placeholder="Paste your resume text here..."
                    rows={10}
                    style={{ resize: "vertical", fontFamily: 'var(--mono)' }}
                />
                <button
                    onClick={handleAnalyse}
                    disabled={loading || !resumeText.trim()}
                    style={{ marginTop: "1rem" }}
                >
                    {loading ? "Analysing..." : "Analyse Resume"}
                </button>
            </div>

            {analysis && (
                <div className="card" style={{ marginTop: "2rem", whiteSpace: "pre-wrap" }}>
                    <h3 style={{ color: 'var(--accent)', marginBottom: '1rem' }}>Analysis Result</h3>
                    <p style={{ lineHeight: '1.8' }}>{analysis}</p>
                </div>
            )}
        </div>
    );
}

export default ResumeAnalyser;
