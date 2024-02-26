import { GoAlertFill } from "react-icons/go";
import "../styles/Switch.css";

interface Props {
  isOn: boolean;
  handleToggle: () => void;
}

const Switch = ({ isOn, handleToggle }: Props) => {
  return (
    <>
      <input
        checked={isOn}
        onChange={handleToggle}
        className="react-switch-checkbox"
        id={`react-switch-new`}
        type="checkbox"
      />
      <label
        style={{ background: isOn ? "#f44336" : "" }}
        className="react-switch-label"
        htmlFor={`react-switch-new`}
      >
        <span className="react-switch-button icon-wrapper">
          <GoAlertFill size={16} className="icon-red mb-1" />
        </span>
      </label>
    </>
  );
};

export default Switch;
