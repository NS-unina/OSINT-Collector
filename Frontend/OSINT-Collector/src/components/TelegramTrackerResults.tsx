import { useState } from "react";
import { TelegramMessage } from "../types/results";
import { MdOpenInNew } from "react-icons/md";
import { IoCalendar } from "react-icons/io5";
import { format } from "date-fns";

interface Props {
  results: TelegramMessage[];
  channelUsername: string;
}

const TelegramTrackerResults = ({ results, channelUsername }: Props) => {
  const [showAll, setShowAll] = useState(true);

  const sortedMessages = [...results].sort((a, b) => {
    if (a.id < b.id) return -1;
    if (a.id > b.id) return 1;
    return 0;
  });

  const filteredPosts = showAll
    ? sortedMessages
    : sortedMessages.filter((message) => message.processed);

  return (
    <div>
      <div className="d-flex justify-content-center align-items-center mb-4">
        <button
          className={`btn mx-2 ${
            showAll ? "btn-primary" : "btn-outline-primary"
          }`}
          onClick={() => setShowAll(true)}
        >
          All messages
        </button>
        <button
          className={`btn mx-2 ${
            !showAll ? "btn-danger" : "btn-outline-danger"
          }`}
          onClick={() => setShowAll(false)}
        >
          Marked messages
        </button>
      </div>
      <div className="row mt-3">
        {filteredPosts.map((message) => (
          <div key={message.id} className="col-sm-6 mb-3 mb-sm-3">
            <a
              href={"https://t.me/" + channelUsername + "/" + message.id}
              target="_blank"
              className="card-link position-relative"
            >
              <div className="card h-100 w-100">
                <div className="card-body snscrape text-center">
                  <h6 className="card-subtitle mb-2 text-body-secondary">
                    @{message.from_id}
                  </h6>
                  <p className="card-text">"{message.message}"</p>
                  <div className="d-flex flex-wrap align-items-center">
                    <div className="me-2">
                      <IoCalendar className="ms-3" />{" "}
                      {format(new Date(message.date), "dd/MM/yyyy, HH:mm")}
                    </div>
                  </div>
                  {message.categories && message.categories.length > 0 && (
                    <div className="d-flex flex-wrap mt-2">
                      {message.categories.map((category) => (
                        <div
                          key={category.uri}
                          className="badge bg-danger me-1 mb-1"
                          role="alert"
                        >
                          {category.name}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
                <MdOpenInNew className="position-absolute top-0 end-0 mt-2 me-2 invisible" />
              </div>
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TelegramTrackerResults;
