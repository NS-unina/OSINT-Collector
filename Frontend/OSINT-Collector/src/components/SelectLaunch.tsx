import { IoCalendar } from "react-icons/io5";
import { Launch } from "../types";
import { useEffect, useState } from "react";

interface Props {
  launches: Launch[];
  selectedLaunch: Launch | null;
  handleLaunchToggle: (launchId: number) => void;
}

const SelectLaunch = ({
  launches,
  selectedLaunch,
  handleLaunchToggle,
}: Props) => {
  const [sortedLaunches, setSortedLaunches] = useState<Launch[]>([]);

  useEffect(() => {
    const sorted = [...launches].sort((a, b) => {
      // Ordina i lanci in ordine decrescente di timestamp
      return new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime();
    });
    setSortedLaunches(sorted);
  }, [launches]);

  return (
    <div>
      <div
        className="mb-3"
        id="launchesContainer"
        style={{ maxHeight: "500px", overflowY: "scroll" }}
      >
        <label className="form-label">Launches:</label>
        {sortedLaunches.map((launch) => (
          <div key={launch.id} className="mb-2">
            <input
              type="checkbox"
              className="btn-check"
              id={`tool-${launch.id}`}
              value={launch.id.toString()}
              autoComplete="off"
              checked={selectedLaunch?.id === launch.id}
              onChange={() => handleLaunchToggle(launch.id)}
            />
            <label
              className="btn btn-outline-success tool-label"
              htmlFor={`tool-${launch.id}`}
            >
              <div className="me-2">
                <IoCalendar className="ms-3" /> {launch.timestamp}
              </div>
              {launch.entrypoint} {">"}
              {" ["}
              {[
                launch.inputs.slice(0, -1).map((input) => {
                  return input + "; ";
                }),
                launch.inputs.slice(-1),
              ]}
              {"]"}
            </label>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SelectLaunch;
