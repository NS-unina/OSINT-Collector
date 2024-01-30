import { RequiredInput, RunToolForm } from "../types";

import { AiFillInstagram, AiFillTwitterCircle } from "react-icons/ai";
import { FaTelegram } from "react-icons/fa";
import { CgDarkMode } from "react-icons/cg";
import { useState } from "react";
import axios from "axios";

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
      return null;
  }
};

const RequiredInputs = ({ requiredInputs, onSubmit }: Props) => {
  const [formData, setFormData] = useState<RunToolForm[]>([]);

  const handleChange = (
    toolName: string,
    capabilityName: string,
    value: string,
    inputIndex: number
  ) => {
    setFormData((prevData) => {
      const existingToolIndex = prevData.findIndex(
        (data) => data.image === toolName && data.entrypoint === capabilityName
      );

      if (existingToolIndex !== -1) {
        const updatedData = [...prevData];
        const existingTool = { ...updatedData[existingToolIndex] };

        // Overwrite the value for the specific input index
        existingTool.inputs[inputIndex] = value;

        updatedData[existingToolIndex] = existingTool;
        return updatedData;
      } else {
        const newToolData: RunToolForm = {
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
      axios
        .post<RunToolForm[]>("http://localhost:5000/launch", formData)
        .then(() => {
          onSubmit();
          setFormData([]);
        })
        .catch((error) => {
          console.error("Error removing tool:", error);
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
          Submit
        </button>
      </form>
    </div>
  );
};

export default RequiredInputs;
