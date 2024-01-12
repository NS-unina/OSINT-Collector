import React, { useEffect } from "react";
import { BiSolidError } from "react-icons/bi";
import { MdDone } from "react-icons/md";

interface AlertMessageProps {
  message: string;
  type: "success" | "danger";
  onClose: () => void;
}

const AlertMessage: React.FC<AlertMessageProps> = ({
  message,
  type,
  onClose,
}) => {
  useEffect(() => {
    // Nascondi il messaggio dopo 5 secondi
    const timer = setTimeout(() => {
      onClose();
    }, 5000);

    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div
      className={`alert alert-dismissible fade show alert-${type} mt-3`}
      role="alert"
    >
      {type == "success" ? <MdDone /> : <BiSolidError />}
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
