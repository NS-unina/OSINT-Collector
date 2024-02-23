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
import LocationCategoryInferenceCard from "./LocationCategoryInferenceCard";
import InstaloaderProfileInfo from "./InstaloaderProfileInfo";
import UsernameInferenceCard from "./UsernameInferenceCard";

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
  const [selectedCardIndex, setSelectedCardIndex] = useState<number | null>(
    null
  );

  const handleSendRequest = (endpoint: string, inputs: string[]) => {
    const inputParams = inputs
      .map((input, index) => `input${index + 1}=${encodeURIComponent(input)}`)
      .join("&");
    const url = `http://localhost:8080/inference/${endpoint}?${inputParams}`;
    axios
      .get(url)
      .then((response) => {
        setInferenceResults(response.data);
      })
      .catch((error) => {
        console.error(`Error sending GET request to ${url}:`, error);
      });
  };

  const handleCloseInput = () => {
    setInferenceResults([]);
  };

  const handleCloseCard = () => {
    setSelectedCardIndex(null);
  };

  const handleSelectedCard = (id: number) => {
    setSelectedCardIndex(id);
  };

  return (
    <div className="container mt-4">
      <div className="row mt-3">
        {(selectedCardIndex === null || selectedCardIndex === 1) && (
          <InferenceCard
            id={1}
            title="Finds all posts that refers directly or indirectly to [category]"
            tags={["category"]}
            endpoint="categories"
            onSendRequest={handleSendRequest}
            handleCloseInput={handleCloseInput}
            handleCloseCard={handleCloseCard}
            setSelectedCard={handleSelectedCard}
          />
        )}
        {(selectedCardIndex === null || selectedCardIndex === 2) && (
          <LocationCategoryInferenceCard
            id={2}
            title="Finds all users who have been to [location] and referred to [category]"
            tags={["location", "category"]}
            endpoints={["categories", "locations"]}
            onSendRequest={handleSendRequest}
            handleCloseInput={handleCloseInput}
            handleCloseCard={handleCloseCard}
            setSelectedCard={handleSelectedCard}
          />
        )}
        {(selectedCardIndex === null || selectedCardIndex === 3) && (
          <UsernameInferenceCard
            id={3}
            title="Finds all users who tagged [account]"
            tags={["account"]}
            endpoint="instagram/accounts"
            onSendRequest={handleSendRequest}
            handleCloseInput={handleCloseInput}
            handleCloseCard={handleCloseCard}
            setSelectedCard={handleSelectedCard}
          />
        )}
      </div>
      <div className="d-flex justify-content-center align-items-center">
        <div className="row mt-4">
          {selectedCardIndex === 1 ? (
            inferenceResults.map((result, index) => (
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
            ))
          ) : (
            <div className="row mt-3">
              {inferenceResults.map(
                (result, index) =>
                  isInstagramAccount(result.account) && (
                    <div key={index} className="col-sm-4 mb-3 mb-sm-3">
                      <InstaloaderProfileInfo {...result.account} />
                    </div>
                  )
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Inference;
