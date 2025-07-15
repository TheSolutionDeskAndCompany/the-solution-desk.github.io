import React from "react";
import { useParams } from "react-router-dom";
import CommentsThread from "./CommentsThread";

export default function CommentsThreadWrapper() {
  const { id } = useParams();

  return (
    <div className="comments-wrapper cyberpunk-theme">
      <h2 className="entity-title">Comments for Entity #{id}</h2>
      <CommentsThread entityId={id} />
    </div>
  );
}
