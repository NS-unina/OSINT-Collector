import { useState, ReactElement } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import { BsCursor, BsTrash, BsPlus } from "react-icons/bs"; // Import delle icone
import SelectTool from "./components/SelectTool";
import RemoveTool from "./components/RemoveTool";
import AddTool from "./components/AddTool";

const App = () => {
  const [selectedTool, setSelectedTool] = useState<string>("");

  const handleSelectTool = (tool: string) => {
    setSelectedTool((prevSelectedTool) =>
      prevSelectedTool === tool ? "" : tool
    );
  };

  const renderPage = (): ReactElement => {
    switch (selectedTool) {
      case "Select Tool":
        return <SelectTool />;
      case "Delete Tool":
        return <RemoveTool />;
      case "Add Tool":
        return <AddTool />;
      default:
        return <div></div>;
    }
  };

  return (
    <div className="container mt-5">
      <header className="text-center mb-4">
        <h1 className="display-4">OSINT Collector</h1>
      </header>
      <div className="row row-cols-1 row-cols-md-3 g-4">
        <div className="col">
          <div
            className={`card h-100 ${
              selectedTool === "Select Tool" ? "border-primary selected" : ""
            }`}
            onClick={() => handleSelectTool("Select Tool")}
          >
            <div className="card-body text-center">
              <BsCursor size={40} className="mb-3 text-primary" />
              <h5 className="card-title">Select Tool</h5>
            </div>
          </div>
        </div>
        <div className="col">
          <div
            className={`card h-100 ${
              selectedTool === "Delete Tool" ? "border-danger selected" : ""
            }`}
            onClick={() => handleSelectTool("Delete Tool")}
          >
            <div className="card-body text-center">
              <BsTrash size={40} className="mb-3 text-danger" />
              <h5 className="card-title">Remove Tool</h5>
            </div>
          </div>
        </div>
        <div className="col">
          <div
            className={`card h-100 ${
              selectedTool === "Add Tool" ? "border-success selected" : ""
            }`}
            onClick={() => handleSelectTool("Add Tool")}
          >
            <div className="card-body text-center">
              <BsPlus size={50} className="mb-3 text-success" />
              <h5 className="card-title">Add Tool</h5>
            </div>
          </div>
        </div>
      </div>
      {selectedTool && <div className="mt-4 fade-in">{renderPage()}</div>}
    </div>
  );
};

export default App;
