import axios from "axios";
import InferenceCard from "./InferenceCard";
import { useState } from "react";
import { MdOpenInNew } from "react-icons/md";

interface InferenceResult {
  shortcode: string;
  text: string;
  url: string;
}

const Inference = () => {
  const [inferenceResults, setInferenceResults] = useState<InferenceResult[]>(
    []
  );

  const handleSendRequest = (endpoint: string, input: string) => {
    axios
      .get(`http://localhost:8080/inference/${endpoint}?input=${input}`)
      .then((response) => {
        setInferenceResults(response.data);
        console.log("Richiesta GET inviata con successo:", response);
      })
      .catch((error) => {
        console.error("Errore durante l'invio della richiesta GET:", error);
      });
  };

  const handleClose = () => {
    setInferenceResults([]);
  };

  return (
    <div className="container mt-4">
      <div className="row mt-3">
        <InferenceCard
          title="Find all posts that refer directly or indirectly to "
          tag="category"
          endpoint="categories"
          onSendRequest={handleSendRequest}
          handleClose={handleClose}
        />
      </div>
      <div className="d-flex justify-content-center align-items-center">
        <div className="row mt-4">
          {inferenceResults.map((result, index) => (
            <div key={index} className="col-sm-4 mb-3">
              <a
                href={
                  result.shortcode
                    ? "https://www.instagram.com/p/" + result.shortcode
                    : result.url
                }
                target="_blank"
                className="card-link position-relative"
              >
                <div className="card h-100 w-100">
                  <div className="card-body snscrape text-center">
                    <p
                      id="cardText"
                      className="card-text p-1"
                      style={{ maxHeight: "300px", overflowY: "scroll" }}
                    >
                      "{result.text}"
                    </p>
                  </div>
                  <MdOpenInNew className="position-absolute top-0 end-0 mt-2 me-2 invisible" />
                </div>
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Inference;
