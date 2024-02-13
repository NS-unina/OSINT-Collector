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
      <div
        className="mb-3"
        id="launchesContainer"
        style={{ maxHeight: "400px", overflowY: "scroll" }}
      >
        <label className="form-label">Launches:</label>
        {launches.map((launch) => (
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
