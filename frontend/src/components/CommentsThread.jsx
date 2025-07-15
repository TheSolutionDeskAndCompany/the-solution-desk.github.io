import React, { useEffect, useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import "./CommentsThread.css";

export default function CommentsThread({ entityId }) {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const fetchComments = async () => {
      setLoading(true);
      try {
        const res = await axios.get(
          `${process.env.REACT_APP_API_URL}/entities/${entityId}/comments`,
        );
        setComments(res.data);
        setError(null);
      } catch (err) {
        console.error("Failed to load comments:", err);
        setError("Failed to load comments");
        toast.error("Could not load comments");
      } finally {
        setLoading(false);
      }
    };

    fetchComments();
  }, [entityId]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!newComment.trim()) return;

    setSubmitting(true);
    setError(null);

    try {
      const res = await axios.post(
        `${process.env.REACT_APP_API_URL}/entities/${entityId}/comments`,
        { text: newComment },
      );
      setComments([...comments, res.data]);
      setNewComment("");
      toast.success("Comment posted successfully");
    } catch (err) {
      console.error("Could not post comment:", err);
      setError("Could not post comment");
      toast.error("Failed to post comment");
    } finally {
      setSubmitting(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  };

  return (
    <div className="comments-container cyberpunk-theme">
      <h3 className="comments-title">Comments</h3>

      {error && <div className="error-message">{error}</div>}

      <div className="comments-list-container">
        {loading ? (
          <div className="comments-loading">Loading comments...</div>
        ) : comments.length === 0 ? (
          <div className="no-comments">
            No comments yet. Be the first to comment!
          </div>
        ) : (
          <ul className="comments-list">
            {comments.map((comment) => (
              <li key={comment.id} className="comment-item">
                <div className="comment-header">
                  <span className="comment-author">
                    {comment.author || "Anonymous"}
                  </span>
                  <span className="comment-date">
                    {formatDate(comment.createdAt || new Date())}
                  </span>
                </div>
                <div className="comment-text">{comment.text}</div>
              </li>
            ))}
          </ul>
        )}
      </div>

      <form onSubmit={handleSubmit} className="comment-form">
        <input
          type="text"
          placeholder="Write a comment…"
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          disabled={submitting}
          aria-label="Comment text"
        />
        <button
          type="submit"
          disabled={!newComment.trim() || submitting}
          className="submit-button"
        >
          {submitting ? (
            <span className="button-spinner" aria-hidden="true"></span>
          ) : (
            "Post"
          )}
        </button>
      </form>
    </div>
  );
}
