import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("https://resume-parser-62d6.onrender.com//upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setResult(data.content || "No text extracted");
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Resume Parser</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <pre>{result}</pre>
    </div>
  );
}

export default App;
