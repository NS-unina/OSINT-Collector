import { useEffect, useState } from "react";
import { Launch } from "../types";
import axios from "axios";
import SelectLaunch from "./SelectLaunch";
import ShowResults from "./ShowResults";

const Results = () => {
  const [launches, setLaunches] = useState<Launch[]>([]);
  const [selectedLaunch, setSelectedLaunch] = useState<Launch | null>(null);

  useEffect(() => {
    axios
      .get<Launch[]>(`http://localhost:8080/launches`)
      .then((res) => setLaunches(res.data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  const handleLaunchToggle = (launchId: number) => {
    const selected = launches.find((l) => l.id === launchId);

    if (selectedLaunch && selectedLaunch.id === launchId) {
      setSelectedLaunch(null);
    } else if (selected) {
      setSelectedLaunch(selected);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row">
        {!selectedLaunch && (
          <SelectLaunch
            launches={launches}
            selectedLaunch={selectedLaunch}
            handleLaunchToggle={handleLaunchToggle}
          />
        )}
        {selectedLaunch && (
          <SelectLaunch
            launches={[selectedLaunch]}
            selectedLaunch={selectedLaunch}
            handleLaunchToggle={handleLaunchToggle}
          />
        )}
        <ShowResults selectedLaunch={selectedLaunch} />
      </div>
    </div>
  );
};

export default Results;
