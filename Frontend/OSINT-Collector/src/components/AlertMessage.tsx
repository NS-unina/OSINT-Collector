import React, { useEffect } from "react";
import { BiSolidError } from "react-icons/bi";
import { MdDone } from "react-icons/md";

interface AlertMessageProps {
  message: string;
  type: "success" | "danger" | "primary";
  time?: number;
  onClose: () => void;
}

const AlertMessage: React.FC<AlertMessageProps> = ({
  message,
  type,
  onClose,
  time = 5000,
}) => {
  useEffect(() => {
    // Nascondi il messaggio dopo "time" secondi
    const timer = setTimeout(() => {
      onClose();
    }, time);

    return () => clearTimeout(timer);
  }, [onClose, time]);

  return (
    <div
      className={`alert alert-dismissible fade show alert-${type} mt-3`}
      role="alert"
    >
      {type === "success" || type === "primary" ? <MdDone /> : <BiSolidError />}
      {message}
      <button
        type="button"
        className="btn-close"
        data-bs-dismiss="alert"
        aria-label="Close"
        onClick={onClose}
      ></button>
    </div>
  );
};

export default AlertMessage;
