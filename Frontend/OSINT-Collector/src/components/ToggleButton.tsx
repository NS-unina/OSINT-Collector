import { useState } from "react";

export default function ToggleButton() {
  const [isToggled, setIsToggled] = useState(false);

  const handleChange = () => {
    setIsToggled(!isToggled);
  };

  return (
    <button
      onClick={handleChange}
      className={`toggle-button ${isToggled ? "on" : "off"}`}
    >
      {isToggled ? "ON" : "OFF"}
    </button>
  );
}
