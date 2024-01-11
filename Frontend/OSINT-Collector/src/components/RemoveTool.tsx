import { useEffect, useState } from "react";
import { GetToolsResponse, Tool } from "../types";
import axios from "axios";

const RemoveTool = () => {
  const [tools, fetchTools] = useState<Tool[]>([]);
  const [selectedTool, setSelectedTool] = useState<Tool | null>(null);

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

    // Esegui l'azione di rimozione qui utilizzando l'elenco selectedTool
    console.log("Tool to remove:", selectedTool);

    // Aggiungi qui la logica per rimuovere lo strumento selezionato
    if (selectedTool) {
      const formData = {
        remove_tool: selectedTool.name,
      };

      axios
        .post<Tool[]>("http://127.0.0.1:5000/remove", formData)
        .then((response) => {
          fetchTools(response.data);
          setSelectedTool(null); // Deseleziona lo strumento dopo la rimozione
        })
        .catch((error) => {
          console.error("Error removing tool:", error);
        });
    }
  };

  return (
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
      <button type="submit" className="btn btn-danger" disabled={!selectedTool}>
        Remove
      </button>
    </form>
  );
};

export default RemoveTool;
