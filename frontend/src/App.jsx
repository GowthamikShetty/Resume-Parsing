import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF file first.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`https://resume-parser-62d6.onrender.com/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");
      const data = await response.json();
      setText(data.content || "No text extracted");
    } catch (error) {
      console.error("Error:", error);
      setText("Error connecting to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Resume Parser</h1>

      {/* ✅ File input with proper label */}
      <label htmlFor="resumeUpload" style={{ display: "block", marginBottom: "8px" }}>
        Upload your Resume (PDF)
      </label>
      <input
        id="resumeUpload"
        type="file"
        accept="application/pdf"
        onChange={handleFileChange}
        title="Choose PDF file"
        aria-label="Choose a resume file to upload"
      />

      {/* ✅ Accessible button */}
      <button
        onClick={handleUpload}
        style={{ marginLeft: "10px" }}
        aria-label="Upload and extract resume text"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>

      <div style={{ marginTop: "20px" }}>
        {loading ? <p>Extracting text...</p> : <pre>{text}</pre>}
      </div>
    </div>
  );
}

export default App;
