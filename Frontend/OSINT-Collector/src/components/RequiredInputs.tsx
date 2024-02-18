import { RequiredInput, RunToolForm } from "../types";
import { format } from "date-fns";
import { AiFillInstagram, AiFillTwitterCircle } from "react-icons/ai";
import { FaTelegram, FaGlobe } from "react-icons/fa";
import { CgDarkMode } from "react-icons/cg";
import { useState } from "react";
import axios from "axios";
import AlertMessage from "./AlertMessage";

interface Props {
  requiredInputs: RequiredInput[];
  onSubmit: () => void;
}

const getPlatformIcon = (platform: string) => {
  switch (platform.toLowerCase()) {
    case "instagram":
      return <AiFillInstagram />;
    case "twitter":
      return <AiFillTwitterCircle />;
    case "telegram":
      return <FaTelegram />;
    case "darkweb":
      return <CgDarkMode />;
    default:
      return <FaGlobe />;
  }
};

const RequiredInputs = ({ requiredInputs, onSubmit }: Props) => {
  const [formData, setFormData] = useState<RunToolForm[]>([]);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const handleChange = (
    toolName: string,
    capabilityName: string,
    value: string,
    inputIndex: number
  ) => {
    setFormData((prevData) => {
      const timestamp = format(new Date(), "yyyy-MM-dd HH:mm"); // Ottieni la data attuale formattata

      const existingToolIndex = prevData.findIndex(
        (data) => data.image === toolName && data.entrypoint === capabilityName
      );

      if (existingToolIndex !== -1) {
        const updatedData = [...prevData];
        const existingTool = { ...updatedData[existingToolIndex] };

        existingTool.inputs[inputIndex] = value;

        updatedData[existingToolIndex] = existingTool;
        return updatedData;
      } else {
        const newToolData: RunToolForm = {
          timestamp: timestamp,
          image: toolName,
          entrypoint: capabilityName,
          inputs: [value],
        };
        return [...prevData, newToolData];
      }
    });
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (formData) {
      formData.forEach((data) => {
        axios
          .post<RunToolForm[]>("http://localhost:8080/launches/save", data, {
            headers: {
              "Content-Type": "application/json",
            },
          })
          .then(() => {
            onSubmit();
            axios.post<RunToolForm[]>("http://localhost:5000/launch", data, {
              headers: {
                "Content-Type": "application/json",
              },
            });
          })
          .catch(() => {
            setSubmitError(" Error running tool. Please try again.");
          });
        setFormData([]);
      });
    }
  };

  return (
    <div className="col-md-6">
      <form onSubmit={handleSubmit}>
        {requiredInputs.map((input, index) => (
          <div key={index}>
            <h3>
              {getPlatformIcon(input.tool.platform)} {input.tool.name}
            </h3>
            <h6 className="mb-3">({input.capability.name})</h6>
            <input
              hidden
              readOnly
              type="text"
              id={input.capability.name}
              value={input.capability.name}
            />
            {input.inputs.map((inputField, inputIndex) => (
              <div key={inputIndex} className="mb-3">
                <input
                  type="text"
                  className="form-control"
                  placeholder={inputField.name}
                  id={inputField.name}
                  onChange={(e) =>
                    handleChange(
                      input.tool.name,
                      input.capability.name,
                      e.target.value,
                      inputIndex
                    )
                  }
                />
              </div>
            ))}
          </div>
        ))}
        <button type="submit" className="btn btn-primary">
          Launch
        </button>
      </form>
      {submitError && (
        <AlertMessage
          message={submitError}
          type="danger"
          onClose={() => setSubmitError(null)}
        />
      )}
    </div>
  );
};

export default RequiredInputs;
