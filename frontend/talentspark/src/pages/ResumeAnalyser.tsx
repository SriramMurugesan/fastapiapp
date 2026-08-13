import { useState } from "react";
import { analyseResume, uploadResumeToS3 } from "../Services/RagService";

function ResumeAnalyser() {
    // Paste Text Analyser States
    const [resumeText, setResumeText] = useState("");
    const [analysis, setAnalysis] = useState("");
    const [loading, setLoading] = useState(false);

    // S3 Upload States
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [uploadResult, setUploadResult] = useState<{
        success: boolean;
        mode: string;
        message: string;
        filename: string;
        url: string;
        db_id?: number;
        user_id?: number;
        local_path?: string;
    } | null>(null);

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

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            setSelectedFile(e.target.files[0]);
            setUploadResult(null); // Clear previous result
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) return;
        setUploading(true);
        try {
            const result = await uploadResumeToS3(selectedFile);
            setUploadResult(result);
        } catch (error) {
            console.error("Upload error:", error);
            alert("File upload failed. Check backend console logs.");
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="page-container" style={{ marginTop: '2rem' }}>
            <h2>Resume Analyser & S3 Storage Demo</h2>

            {/* Pasta Text Analyser Section */}
            <div className="card">
                <h3>Option 1: Paste Resume Text for AI Analysis</h3>
                <textarea
                    value={resumeText}
                    onChange={(e) => setResumeText(e.target.value)}
                    placeholder="Paste your resume text here..."
                    rows={10}
                    style={{ resize: "vertical", fontFamily: 'var(--mono)', width: '100%', marginBottom: '1rem' }}
                />
                <button
                    onClick={handleAnalyse}
                    disabled={loading || !resumeText.trim()}
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

            {/* AWS S3 Upload Demo Section */}
            <div className="card" style={{ marginTop: '3rem' }}>
                <h3>Option 2: AWS S3 Resume Storage Demo 📁</h3>
                <p style={{ fontSize: '0.95rem', opacity: 0.85, marginBottom: '1.5rem' }}>
                    This features demonstrates how to upload physical files to cloud storage like <strong>Amazon S3</strong>. 
                    If AWS credentials are not configured, it falls back to saving files locally while simulating the S3 response structure.
                </p>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: '500px' }}>
                    <input 
                        type="file" 
                        onChange={handleFileChange}
                        accept=".txt,.pdf,.doc,.docx"
                        style={{
                            padding: '0.5rem',
                            border: '1px dashed var(--border)',
                            borderRadius: 'var(--radius-sm)',
                            cursor: 'pointer'
                        }}
                    />
                    
                    <button
                        onClick={handleUpload}
                        disabled={uploading || !selectedFile}
                        style={{ alignSelf: 'flex-start' }}
                    >
                        {uploading ? "Uploading to S3..." : "Upload File"}
                    </button>
                </div>

                {uploadResult && (
                    <div style={{ 
                        marginTop: '2rem', 
                        padding: '1.5rem', 
                        border: '1px solid var(--border)', 
                        borderRadius: 'var(--radius-sm)',
                        background: 'rgba(255, 255, 255, 0.03)'
                    }}>
                        <h4 style={{ 
                            color: uploadResult.mode.includes("Production") ? 'var(--success)' : 'var(--accent)', 
                            marginTop: 0,
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem'
                        }}>
                            <span>●</span> {uploadResult.mode}
                        </h4>
                        
                        <p style={{ margin: '0.5rem 0', lineHeight: '1.6' }}>
                            {uploadResult.message}
                        </p>

                        <div style={{ marginTop: '1rem' }}>
                            <p style={{ margin: '0.25rem 0' }}><strong>File Name:</strong> {uploadResult.filename}</p>
                            <p style={{ margin: '0.25rem 0', wordBreak: 'break-all' }}>
                                <strong>Simulated S3 Link:</strong>{' '}
                                <a 
                                    href={uploadResult.url} 
                                    target="_blank" 
                                    rel="noreferrer"
                                    style={{ color: 'var(--accent)', textDecoration: 'underline' }}
                                >
                                    {uploadResult.url}
                                </a>
                            </p>
                            {uploadResult.db_id && (
                                <p style={{ margin: '0.25rem 0' }}>
                                    <strong>PostgreSQL DB ID:</strong> <code>{uploadResult.db_id}</code> (Associated with User ID: <code>{uploadResult.user_id}</code>)
                                </p>
                            )}
                            {uploadResult.local_path && (
                                <p style={{ margin: '0.25rem 0', color: 'var(--text)' }}>
                                    <strong>Saved Path (Backend):</strong> <code>{uploadResult.local_path}</code>
                                </p>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default ResumeAnalyser;
