import { RequiredInput } from "../types";

import { AiFillInstagram, AiFillTwitterCircle } from "react-icons/ai";
import { FaTelegram } from "react-icons/fa";
import { CgDarkMode } from "react-icons/cg";

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
  return (
    <div className="col-md-6">
      <form>
        {requiredInputs.map((input, index) => (
          <div key={index}>
            <h3>
              {getPlatformIcon(input.tool.platform)} {input.tool.name}
            </h3>
            {input.input.map((inputField) => (
              <div key={inputField.name} className="mb-3">
                <label htmlFor={inputField.name} className="form-label">
                  {inputField.label}
                </label>
                <input
                  type="text"
                  className="form-control"
                  id={inputField.name}
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
