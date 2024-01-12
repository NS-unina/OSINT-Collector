import { Capability } from "../types";

interface Props {
  capabilities: Capability[];
  selectedCapabilities: Capability[];
  handleCapabilityToggle: (capabilityId: number) => void;
}

const SelectCapability = ({
  capabilities,
  selectedCapabilities,
  handleCapabilityToggle,
}: Props) => {
  return (
    <div className="mb-3" id="capabilityContainer">
      <label className="form-label">Capabilities:</label>
      {capabilities.map((capability) => (
        <div key={capability.id} className="mb-2">
          <input
            type="checkbox"
            className="btn-check"
            id={`capability-${capability.id}`}
            value={capability.name}
            autoComplete="off"
            checked={selectedCapabilities.some((c) => c.id === capability.id)}
            onChange={() => handleCapabilityToggle(capability.id)}
          />
          <label
            className="btn btn-outline-primary capability-label"
            htmlFor={`capability-${capability.id}`}
          >
            {capability.name}
          </label>
        </div>
      ))}
    </div>
  );
};

export default SelectCapability;
