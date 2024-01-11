import React, { useEffect, useState } from "react";
import { GetToolsResponse, Tool } from "../types";
import axios from "axios";
import AlertMessage from "./AlertMessage";

const RemoveTool = () => {
  const [tools, fetchTools] = useState<Tool[]>([]);
  const [selectedTool, setSelectedTool] = useState<Tool | null>(null);
  const [removeSuccess, setRemoveSuccess] = useState<boolean | null>(null);

  useEffect(() => {
    axios
      .get<GetToolsResponse>(`http://127.0.0.1:5000/get_tools`)
      .then((res) => fetchTools(res.data.tools))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  const handleToolToggle = (toolId: number) => {
    const selected = tools.find((t) => t.id === toolId);

    if (selected) {
      setSelectedTool(selectedTool === selected ? null : selected);
    }
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();

    if (selectedTool) {
      const formData = {
        remove_tool: selectedTool.name,
      };

      axios
        .post<Tool[]>("http://127.0.0.1:5000/remove", formData)
        .then((response) => {
          fetchTools(response.data);
          setSelectedTool(null);
          setRemoveSuccess(true);
        })
        .catch((error) => {
          console.error("Error removing tool:", error);
          setRemoveSuccess(false);
        });
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="mb-3" id="toolsContainer">
          <label className="form-label">Tools:</label>
          {tools.map((tool) => (
            <div key={tool.id} className="mb-2">
              <input
                type="radio"
                className="btn-check"
                id={`tool-${tool.id}`}
                value={tool.name}
                autoComplete="off"
                checked={selectedTool?.id === tool.id}
                onChange={() => handleToolToggle(tool.id)}
              />
              <label
                className="btn btn-outline-primary"
                htmlFor={`tool-${tool.id}`}
              >
                {tool.name}
              </label>
            </div>
          ))}
        </div>
        <button
          type="submit"
          className="btn btn-danger"
          disabled={!selectedTool}
        >
          Remove
        </button>
      </form>
      {removeSuccess !== null && (
        <AlertMessage
          message={
            removeSuccess
              ? "Tool removed successfully!"
              : "Error removing tool."
          }
          type={removeSuccess ? "success" : "danger"}
          onClose={() => setRemoveSuccess(null)}
        />
      )}
    </div>
  );
};

export default RemoveTool;
