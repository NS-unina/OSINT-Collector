import { Launch } from "../types";

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
  return (
    <div>
      <div className="mb-3" id="launchesContainer">
        <label className="form-label">Launches:</label>
        {launches.map((launch) => (
          <div key={launch.id} className="mb-2">
            <input
              type="checkbox"
              className="btn-check"
              id={`tool-${launch.id}`}
              value={launch.id.toString()} // Usiamo l'id come valore per il checkbox
              autoComplete="off"
              checked={selectedLaunch?.id === launch.id}
              onChange={() => handleLaunchToggle(launch.id)}
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

export default SelectLaunch;
