import React, { useEffect, useState } from "react";
import axios from "axios";
import SelectCapability from "./SelectCapability";
import { Platform, Capability, RequiredInput } from "../types";
import RequiredInputs from "./RequiredInputs";
import { Player, Controls } from "@lottiefiles/react-lottie-player";
import AlertMessage from "./AlertMessage";
import "../App.css";

const SelectTool = () => {
  const [platforms, setPlatforms] = useState<Platform[]>([]);
  const [capabilities, setCapabilities] = useState<Capability[]>([]);
  const [selectedCapabilities, setSelectedCapabilities] = useState<
    Capability[]
  >([]);
  const [requiredInputs, setRequiredInputs] = useState<RequiredInput[]>([]);
  const [selectedPlatform, setSelectedPlatform] = useState<string>("All");
  const [submitted, setSubmit] = useState(false);

  useEffect(() => {
    fetchPlatform();
    fetchCapabilities("All");
  }, []);

  const fetchPlatform = () => {
    axios
      .get<Platform[]>(`http://localhost:8080/platforms`)
      .then((res) => setPlatforms(res.data))
      .catch((error) => console.error("Error fetching data:", error));
  };

  const fetchCapabilities = (platform: string) => {
    axios
      .get<Capability[]>(
        `http://localhost:8080/capabilities?platform=${platform}`
      )
      .then((res) => setCapabilities(res.data))
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
    fetchCapabilities(selectedPlatform);
    setSelectedPlatform(selectedPlatform);
  };

  const handleSubmit = () => {
    setSubmit(true);
  };

  useEffect(() => {
    const fetchRequiredInputs = () => {
      if (selectedCapabilities.length > 0) {
        const formData = {
          capabilities: selectedCapabilities.map(
            (capability) => capability.name
          ),
        };

        axios
          .post<RequiredInput[]>(
            "http://localhost:8080/tools/requiredInputs",
            formData
          )
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

  return (
    <div className="container mt-5">
      <div className="row">
        {submitted ? (
          <div>
            <AlertMessage
              message={"Tool launched!"}
              type={"primary"}
              time={8000}
              onClose={() => {
                setSelectedCapabilities([]);
                setSubmit(false);
              }}
            />
            <Player
              autoplay
              loop
              src="https://lottie.host/d4f8ec0d-eadf-42be-a573-f03167697e06/EXDDIB9Rg8.json"
              style={{ height: "300px", width: "300px" }}
              className="fade-in"
            >
              <Controls
                visible={false}
                buttons={["play", "repeat", "frame", "debug"]}
              />
            </Player>
          </div>
        ) : (
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
                {platforms.map((platform) => (
                  <option key={platform.id} value={platform.name}>
                    {platform.name}
                  </option>
                ))}
              </select>
            </div>

            <SelectCapability
              capabilities={capabilities}
              selectedCapabilities={selectedCapabilities}
              handleCapabilityToggle={handleCapabilityToggle}
            />
          </div>
        )}

        {!submitted && requiredInputs.length > 0 && (
          <RequiredInputs
            requiredInputs={requiredInputs}
            onSubmit={handleSubmit}
          />
        )}
      </div>
    </div>
  );
};

export default SelectTool;
