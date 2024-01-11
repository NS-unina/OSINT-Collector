import React, { useEffect, useState } from "react";
import axios from "axios";

import { AiFillInstagram, AiFillTwitterCircle } from "react-icons/ai";
import { FaTelegram } from "react-icons/fa";
import { CgDarkMode } from "react-icons/cg";
import SelectCapability from "./SelectCapability";
import { Capability, RequiredInput, ServerResponse } from "../types";

const SelectTool: React.FC = () => {
  const [capabilities, setCapabilities] = useState<Capability[]>([]);
  const [selectedCapabilities, setSelectedCapabilities] = useState<
    Capability[]
  >([]);
  const [requiredInputs, setRequiredInputs] = useState<RequiredInput[]>([]);
  const [selectedPlatform, setSelectedPlatform] = useState<string>("All");

  useEffect(() => {
    fetchData("All");
  }, []);

  const fetchData = (platform: string) => {
    axios
      .get<ServerResponse>(
        `http://127.0.0.1:5000/get_capabilities?platform=${platform}`
      )
      .then((response) =>
        updateCapabilities(response.data.capability_parameters)
      )
      .catch((error) => console.error("Error fetching data:", error));
  };

  const handleCapabilityToggle = (capabilityId: number) => {
    setSelectedCapabilities((prevSelected) =>
      prevSelected.some((capability) => capability.id === capabilityId)
        ? prevSelected.filter((capability) => capability.id !== capabilityId)
        : [
            ...prevSelected,
            capabilities.find((c) => c.id === capabilityId) || {
              id: capabilityId,
              name: "",
            },
          ]
    );
  };

  const handlePlatformChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const selectedPlatform = event.target.value;
    fetchData(selectedPlatform);
    setSelectedPlatform(selectedPlatform);
  };

  const updateCapabilities = (capabilities: string[]) => {
    setCapabilities(
      capabilities.map((capability, index) => ({
        id: index + 1,
        name: capability,
      }))
    );
  };

  useEffect(() => {
    const fetchRequiredInputs = () => {
      if (selectedCapabilities.length > 0) {
        const formData = {
          platform: selectedPlatform,
          capabilities: selectedCapabilities.map(
            (capability) => capability.name
          ),
        };

        axios
          .post<RequiredInput[]>("http://127.0.0.1:5000/select", formData)
          .then((response) => {
            setRequiredInputs(response.data);
          })
          .catch((error) => {
            console.error("Error fetching required inputs:", error);
          });
      } else {
        setRequiredInputs([]);
      }
    };

    fetchRequiredInputs();
  }, [selectedCapabilities, selectedPlatform]);

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

  return (
    <div className="container mt-5">
      <div className="row">
        <div className="col-md-6">
          <div className="mb-3">
            <label htmlFor="platform" className="form-label">
              Platform:
            </label>
            <select
              className="form-select"
              name="platform"
              id="platform"
              value={selectedPlatform}
              onChange={handlePlatformChange}
            >
              <option value="All">All</option>
              <option value="Instagram">Instagram</option>
              <option value="Twitter">Twitter</option>
              <option value="Telegram">Telegram</option>
              <option value="DarkWeb">DarkWeb</option>
            </select>
          </div>

          <SelectCapability
            capabilities={capabilities}
            selectedCapabilities={selectedCapabilities}
            handleCapabilityToggle={handleCapabilityToggle}
          />
        </div>

        {requiredInputs.length > 0 && (
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
        )}
      </div>
    </div>
  );
};

export default SelectTool;
