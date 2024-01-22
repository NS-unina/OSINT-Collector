import { RequiredInput, RequiredToolInputs } from "../types";

import { AiFillInstagram, AiFillTwitterCircle } from "react-icons/ai";
import { FaTelegram } from "react-icons/fa";
import { CgDarkMode } from "react-icons/cg";
import { useState } from "react";
import axios from "axios";

interface Props {
  requiredInputs: RequiredInput[];
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

const RequiredInputs = ({ requiredInputs }: Props) => {
  const [formData, setFormData] = useState<RequiredToolInputs[]>([]);

  const handleChange = (toolName: string, inputName: string, value: string) => {
    setFormData((prevData) => {
      const toolData = prevData.find((data) => data[toolName]);
      if (toolData) {
        toolData[toolName][inputName] = value;
        return [...prevData];
      } else {
        const newToolData = { [toolName]: { [inputName]: value } };
        return [...prevData, newToolData];
      }
    });
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (formData) {
      axios
        .post<RequiredToolInputs[]>("http://localhost:8080/tools/run", formData)
        .then(() => {
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
            {input.inputs.map((inputField) => (
              <div key={inputField.name} className="mb-3">
                <label htmlFor={inputField.name} className="form-label">
                  {inputField.label}
                </label>
                <input
                  type="text"
                  className="form-control"
                  id={inputField.name}
                  onChange={(e) =>
                    handleChange(
                      input.tool.name,
                      inputField.name,
                      e.target.value
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
