import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [parsedData, setParsedData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setParsedData(null);
    setError("");
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    setLoading(true);
    setError("");
    setParsedData(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("https://resume-parser-62d6.onrender.com/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");
      const data = await response.json();

      // ✅ Correctly handle the backend’s "parsed" structure
      if (data.success && data.parsed) {
        setParsedData(data.parsed);
      } else {
        setError("No data extracted. Try another resume.");
      }
    } catch (err) {
      console.error("Error:", err);
      setError("Error connecting to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif", maxWidth: "700px", margin: "auto" }}>
      <h1 style={{ marginBottom: "20px" }}>Resume Parser</h1>

      {/* ✅ File input with accessible label */}
      <label htmlFor="resumeUpload" style={{ display: "block", marginBottom: "8px" }}>
        Upload your Resume (PDF, DOCX, or TXT)
      </label>
      <input
        id="resumeUpload"
        type="file"
        accept=".pdf,.docx,.txt"
        onChange={handleFileChange}
        title="Choose a resume file"
        aria-label="Choose a resume file to upload"
      />

      {/* ✅ Accessible Upload Button */}
      <button
        onClick={handleUpload}
        disabled={loading}
        aria-label="Upload and extract resume text"
        style={{
          marginLeft: "10px",
          padding: "8px 16px",
          backgroundColor: "#007bff",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        {loading ? "Uploading..." : "Upload"}
      </button>

      {/* ✅ Feedback and extracted results */}
      <div style={{ marginTop: "20px" }}>
        {loading && <p>Extracting text... please wait ⏳</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}

        {parsedData && (
          <div style={{ marginTop: "20px" }}>
            <h3>Extracted Resume Information:</h3>
            <div style={{ background: "#f4f4f4", padding: "15px", borderRadius: "8px" }}>
              <p><strong>Name:</strong> {parsedData.name || "—"}</p>
              <p><strong>Email(s):</strong> {parsedData.emails?.join(", ") || "—"}</p>
              <p><strong>Phone(s):</strong> {parsedData.phones?.join(", ") || "—"}</p>
              <p><strong>Skills:</strong> {parsedData.skills?.join(", ") || "—"}</p>
              {parsedData.education && (
                <p><strong>Education:</strong> {parsedData.education?.join(", ") || "—"}</p>
              )}
              {parsedData.experience && (
                <p><strong>Experience:</strong> {parsedData.experience?.join(", ") || "—"}</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
