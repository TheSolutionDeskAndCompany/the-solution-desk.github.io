import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import './SOPViewerUploader.css';

export default function SOPViewerUploader() {
  const [file, setFile] = useState(null);
  const [fileList, setFileList] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch existing files on component mount
  useEffect(() => {
    const fetchFiles = async () => {
      try {
        if (process.env.REACT_APP_API_URL) {
          const response = await axios.get(`${process.env.REACT_APP_API_URL}/sop`);
          setFileList(response.data || []);
        }
      } catch (err) {
        console.error('Failed to fetch SOPs:', err);
        setError('Could not load existing SOPs');
      } finally {
        setLoading(false);
      }
    };
    
    fetchFiles();
  }, []);

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      toast.error('Please select a file first');
      return;
    }
    
    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/sop/upload`,
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      setFileList([...fileList, response.data]);
      setFile(null);
      toast.success('File uploaded successfully!');
      
      // Clear file input
      const fileInput = document.getElementById('sop-file-input');
      if (fileInput) fileInput.value = '';
    } catch (err) {
      console.error('Upload failed:', err);
      setError('File upload failed');
      toast.error('Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (fileId) => {
    if (!window.confirm('Are you sure you want to delete this SOP?')) {
      return;
    }

    try {
      await axios.delete(`${process.env.REACT_APP_API_URL}/sop/${fileId}`);
      setFileList(fileList.filter((f) => f.id !== fileId));
      toast.success('File deleted successfully!');
    } catch (err) {
      console.error('Deletion failed:', err);
      setError('File deletion failed');
      toast.error('Could not delete file. Please try again.');
    }
  };

  return (
    <div className="cyberpunk-theme sop-container">
      <h1>Standard Operating Procedures</h1>
      <p className="sop-description">
        Upload, view, and manage company SOPs. All files are securely stored and accessible only to authorized personnel.
      </p>

      <div className="upload-section">
        <h2>Upload New SOP</h2>
        <div className="file-input-container">
          <input 
            type="file" 
            id="sop-file-input"
            onChange={handleFileChange} 
            accept=".pdf,.doc,.docx,.txt"
          />
          <div className="selected-file">
            {file ? `Selected: ${file.name}` : 'No file selected'}
          </div>
        </div>
        <button 
          onClick={handleUpload} 
          disabled={uploading || !file} 
          className="upload-button"
        >
          {uploading ? <span className="spinner" aria-label="Uploading…"></span> : 'Upload SOP'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="sop-list-section">
        <h2>Available SOPs</h2>
        {loading ? (
          <div className="loading">Loading SOPs...</div>
        ) : (
          <div className="file-list">
            {fileList.length === 0 ? (
              <p className="no-files">No SOPs have been uploaded yet.</p>
            ) : (
              <table className="sop-table">
                <thead>
                  <tr>
                    <th>File Name</th>
                    <th>Date Uploaded</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {fileList.map((file) => (
                    <tr key={file.id} className="file-item">
                      <td>
                        <a 
                          href={`${process.env.REACT_APP_API_URL}/sop/${file.id}`} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="file-link"
                        >
                          {file.name}
                        </a>
                      </td>
                      <td>{new Date(file.uploadedAt || Date.now()).toLocaleDateString()}</td>
                      <td>
                        <button 
                          onClick={() => handleDelete(file.id)}
                          className="delete-button"
                          aria-label={`Delete ${file.name}`}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
