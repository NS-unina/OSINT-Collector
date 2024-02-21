import axios from "axios";
import InferenceCard from "./InferenceCard";
import { useState } from "react";
import { MdOpenInNew } from "react-icons/md";
import {
  InstagramAccount,
  InstagramPost,
  TelegramChannel,
  TelegramPost,
} from "../types/results";

import { AiFillInstagram } from "react-icons/ai";
import { FaTelegram } from "react-icons/fa";

interface InferenceResult {
  post: InstagramPost | TelegramPost;
  account: InstagramAccount | TelegramChannel;
}

const isInstagramPost = (
  post: InstagramPost | TelegramPost
): post is InstagramPost => {
  return (post as InstagramPost).shortcode !== undefined;
};

const isInstagramAccount = (
  account: InstagramAccount | TelegramChannel
): account is InstagramAccount => {
  return (account as InstagramAccount).username !== undefined;
};

const Inference = () => {
  const [inferenceResults, setInferenceResults] = useState<InferenceResult[]>(
    []
  );

  const handleSendRequest = (endpoint: string, input: string) => {
    axios
      .get(`http://localhost:8080/inference/${endpoint}?input=${input}`)
      .then((response) => {
        setInferenceResults(response.data);
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
          title="Find all posts that refers directly or indirectly to "
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
                  isInstagramPost(result.post)
                    ? "https://www.instagram.com/p/" + result.post.shortcode
                    : result.post.url
                }
                target="_blank"
                className="card-link position-relative"
              >
                <div className="card h-100 w-100">
                  <div className="card-body snscrape text-center">
                    <h5 className="card-title">
                      {isInstagramPost(result.post) ? (
                        <AiFillInstagram />
                      ) : (
                        <FaTelegram />
                      )}
                      <> </>
                      {isInstagramAccount(result.account)
                        ? result.account.username
                        : result.account.name}
                    </h5>
                    <p
                      id="cardText"
                      className="card-text p-1"
                      style={{ maxHeight: "300px", overflowY: "scroll" }}
                    >
                      "{result.post.text}"
                    </p>
                    <div className="d-flex flex-wrap"></div>
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
