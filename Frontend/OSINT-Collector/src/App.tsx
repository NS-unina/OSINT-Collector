import { useState, ReactElement } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import { BsCursor, BsSearch, BsTrash, BsPlus } from "react-icons/bs";
import { PiGraphDuotone } from "react-icons/pi";
import { SiGraphql } from "react-icons/si";
import SelectTool from "./components/SelectTool";
import RemoveTool from "./components/RemoveTool";
import AddTool from "./components/AddTool";
import Results from "./components/Results";
import Inference from "./components/Inference";
import Switch from "./components/Switch";
import { FaTimes } from "react-icons/fa";
import SearchEngine from "./components/SearchEngine";

const App = () => {
  const [selectedTool, setSelectedTool] = useState<string | null>(null);
  const [showAllTools, setShowAllTools] = useState(false);

  const handleSelectTool = (tool: string) => {
    setSelectedTool((prevSelectedTool) =>
      prevSelectedTool === tool ? null : tool
    );
  };

  const handleToggleView = () => {
    setShowAllTools(!showAllTools);
  };

  const renderPage = (): ReactElement => {
    switch (selectedTool) {
      case "Select Tool":
        return <SelectTool />;
      case "Delete Tool":
        return <RemoveTool />;
      case "Add Tool":
        return <AddTool />;
      case "Results":
        return <Results />;
      case "Search":
        return <SearchEngine />;
      case "Inference":
        return <Inference />;
      default:
        return <div></div>;
    }
  };

  return (
    <div className="container mt-5 mb-5">
      {selectedTool == null && (
        <div className="d-flex justify-content-end align-items-center mb-2">
          <Switch
            type="tools"
            isOn={showAllTools}
            color="green"
            handleToggle={handleToggleView}
          />
        </div>
      )}
      <header className="text-center mb-4">
        <h1 className="display-4">OSINT Collector</h1>
      </header>
      <div className="d-flex justify-content-center">
        <div
          className={
            showAllTools
              ? "row row-cols-1 row-cols-md-2 g-4"
              : "row row-cols-1 row-cols-md-4 g-4"
          }
        >
          {!showAllTools && (
            <>
              <div className="col">
                <div
                  className={`card h-100 ${
                    selectedTool === "Select Tool"
                      ? "border-primary selected"
                      : ""
                  }`}
                  onClick={() => handleSelectTool("Select Tool")}
                >
                  {selectedTool === "Select Tool" && (
                    <div className="position-absolute top-0 start-100 translate-middle mt-1">
                      <div className="icon-wrapper">
                        <FaTimes className="icon-red" />
                      </div>
                    </div>
                  )}
                  <div className="card-body text-center">
                    <BsCursor size={40} className="mb-3 text-primary" />
                    <h5 className="card-title">Select Tool</h5>
                  </div>
                </div>
              </div>
              <div className="col">
                <div
                  className={`card h-100 ${
                    selectedTool === "Search" ? "border-warning selected" : ""
                  }`}
                  onClick={() => handleSelectTool("Search")}
                >
                  {selectedTool === "Search" && (
                    <div className="position-absolute top-0 start-100 translate-middle mt-1">
                      <div className="icon-wrapper">
                        <FaTimes className="icon-red" />
                      </div>
                    </div>
                  )}
                  <div className="card-body text-center">
                    <BsSearch size={40} className="mb-3 text-warning" />
                    <h5 className="card-title">Search</h5>
                  </div>
                </div>
              </div>
              <div className="col">
                <div
                  className={`card h-100 ${
                    selectedTool === "Results" ? "border-success selected" : ""
                  }`}
                  onClick={() => handleSelectTool("Results")}
                >
                  {selectedTool === "Results" && (
                    <div className="position-absolute top-0 start-100 translate-middle mt-1">
                      <div className="icon-wrapper">
                        <FaTimes className="icon-red" />
                      </div>
                    </div>
                  )}
                  <div className="card-body text-center">
                    <PiGraphDuotone size={40} className="mb-3 text-success" />
                    <h5 className="card-title">Results</h5>
                  </div>
                </div>
              </div>
              <div className="col">
                <div
                  className={`card h-100 ${
                    selectedTool === "Inference"
                      ? "border-warning selected"
                      : ""
                  }`}
                  onClick={() => handleSelectTool("Inference")}
                >
                  {selectedTool === "Inference" && (
                    <div className="position-absolute top-0 start-100 translate-middle mt-1">
                      <div className="icon-wrapper">
                        <FaTimes className="icon-red" />
                      </div>
                    </div>
                  )}
                  <div className="card-body text-center">
                    <SiGraphql size={40} className="mb-3 text-warning" />
                    <h5 className="card-title">Inference</h5>
                  </div>
                </div>
              </div>
            </>
          )}
          {showAllTools && (
            <>
              <div className="col">
                <div
                  className={`card h-100 ${
                    selectedTool === "Delete Tool"
                      ? "border-danger selected"
                      : ""
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
            </>
          )}
        </div>
      </div>
      {selectedTool && <div className="mt-4">{renderPage()}</div>}
    </div>
  );
};

export default App;
