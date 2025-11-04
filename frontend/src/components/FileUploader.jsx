import React, { useState } from "react";

export default function FileUploader() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // 🔹 Function to handle upload and parsing
  const onSubmit = async (e) => {
    e.preventDefault();
    if (!file) return setError("Please choose a file first");

    setError("");
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("https://resume-parser-62d6.onrender.com/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || JSON.stringify(data));

      // ✅ Correctly handle backend JSON structure: { success: true, parsed: {...} }
      if (data.success && data.parsed) {
        setResult(data.parsed);
      } else {
        setResult(data);
      }
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  };

  // 🔹 Download JSON result
  const downloadJSON = () => {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "parsed_resume.json";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="p-6 max-w-2xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">Resume Parser</h1>

      <form onSubmit={onSubmit} className="space-y-4">
        {/* ✅ Accessibility label + title for input */}
        <label htmlFor="resumeUpload" className="block font-medium">
          Upload your Resume (PDF, DOCX, or TXT)
        </label>
        <input
          id="resumeUpload"
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={(e) => setFile(e.target.files?.[0])}
          title="Choose resume file"
          className="block border rounded p-2 w-full"
        />

        <div className="flex gap-2">
          <button
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            type="submit"
            title="Upload and parse the selected resume"
          >
            {loading ? "Parsing..." : "Upload & Parse"}
          </button>

          <button
            type="button"
            onClick={downloadJSON}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            disabled={!result}
            title="Download parsed data as JSON"
          >
            Download JSON
          </button>
        </div>
      </form>

      {error && <div className="mt-4 text-red-600">{error}</div>}

      {loading && <div className="mt-4">Parsing... please wait ⏳</div>}

      {result && (
        <div className="mt-6 space-y-4">
          <div className="p-4 border rounded">
            <h3 className="font-semibold text-lg">Name</h3>
            <div>{result.name || "—"}</div>
          </div>

          <div className="p-4 border rounded">
            <h3 className="font-semibold text-lg">Contact</h3>
            <div>Emails: {result.emails?.join(", ") || "—"}</div>
            <div>Phones: {result.phones?.join(", ") || "—"}</div>
          </div>

          <div className="p-4 border rounded">
            <h3 className="font-semibold text-lg">Skills</h3>
            <div className="flex gap-2 flex-wrap">
              {result.skills?.length ? (
                result.skills.map((s) => (
                  <span
                    key={s}
                    className="px-2 py-1 bg-slate-100 rounded border"
                  >
                    {s}
                  </span>
                ))
              ) : (
                "—"
              )}
            </div>
          </div>

          <div className="p-4 border rounded">
            <h3 className="font-semibold text-lg">Education</h3>
            <ul className="list-disc ml-6">
              {result.education?.length ? (
                result.education.map((e, i) => <li key={i}>{e}</li>)
              ) : (
                <li>—</li>
              )}
            </ul>
          </div>

          <div className="p-4 border rounded">
            <h3 className="font-semibold text-lg">Experience</h3>
            {result.experience?.length ? (
              result.experience.map((ex, i) => (
                <p key={i} className="mb-2">
                  {ex}
                </p>
              ))
            ) : (
              <div>—</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
