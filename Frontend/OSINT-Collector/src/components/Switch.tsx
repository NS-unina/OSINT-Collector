import { GoAlertFill } from "react-icons/go";
import { FaTools } from "react-icons/fa";
import "../styles/Switch.css";

interface Props {
  isOn: boolean;
  handleToggle: () => void;
  type: string;
  color: string;
}

const Switch = ({ isOn, handleToggle, type, color }: Props) => {
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
        style={{ background: isOn ? color : "" }}
        className="react-switch-label"
        htmlFor={`react-switch-new`}
      >
        <span className="react-switch-button icon-wrapper">
          {type == "alert" && (
            <GoAlertFill size={16} className="icon-red mb-1" />
          )}
          {type == "tools" && <FaTools size={13} />}
        </span>
      </label>
    </>
  );
};

export default Switch;
