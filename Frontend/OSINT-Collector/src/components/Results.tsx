import { useEffect, useState } from "react";
import { Launch } from "../types";
import axios from "axios";

const Results = () => {
  const [launches, setLaunches] = useState<Launch[]>([]);
  const [selectedLaunch, setSelectedLaunch] = useState<Launch | null>(null);

  useEffect(() => {
    axios
      .get<Launch[]>(`http://localhost:8080/launches`)
      .then((res) => setLaunches(res.data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  const handleToolToggle = (launchId: number) => {
    const selected = launches.find((l) => l.id === launchId);

    if (selected) {
      setSelectedLaunch(selectedLaunch === selected ? null : selected);
    }
  };

  return (
    <div>
      <div className="mb-3 mt-5" id="launchesContainer">
        <label className="form-label">Launches:</label>
        {launches.map((launch) => (
          <div key={launch.id} className="mb-2">
            <input
              type="radio"
              className="btn-check"
              id={`tool-${launch.id}`}
              value={launch.entrypoint}
              autoComplete="off"
              checked={selectedLaunch?.id === launch.id}
              onChange={() => handleToolToggle(launch.id)}
            />
            <label
              className="btn btn-outline-success tool-label"
              htmlFor={`tool-${launch.id}`}
            >
              {launch.entrypoint} {">"} {launch.inputs}
            </label>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Results;
