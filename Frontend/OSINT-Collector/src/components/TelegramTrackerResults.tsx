import { useState } from "react";
import axios from "axios";
import { MdOpenInNew } from "react-icons/md";
import { IoCalendar } from "react-icons/io5";
import { format } from "date-fns";
import { TelegramMessage } from "../types/results";

interface Props {
  results: TelegramMessage[];
  channelUsername: string;
}

const TelegramTrackerResults = ({ results, channelUsername }: Props) => {
  const [hoveredMessageId, setHoveredMessageId] = useState<string | null>(null);
  const [showAll, setShowAll] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const postsPerPage = 10;
  const totalPages = Math.ceil(results.length / postsPerPage);

  const sortedMessages = [...results].sort((a, b) => {
    if (a.id < b.id) return -1;
    if (a.id > b.id) return 1;
    return 0;
  });

  const filteredPosts = showAll
    ? sortedMessages
    : sortedMessages.filter((message) => message.processed);

  const indexOfLastPost = currentPage * postsPerPage;
  const indexOfFirstPost = indexOfLastPost - postsPerPage;
  const currentPosts = filteredPosts.slice(indexOfFirstPost, indexOfLastPost);

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber);

  const handleUsernameAnalysisClick = (username: string) => {
    const requestBody = {
      timestamp: format(new Date(), "yyyy-MM-dd HH:mm"),
      image: "blackbird",
      entrypoint: "search-accounts",
      inputs: [username],
    };

    axios
      .post("http://localhost:5000/launch", requestBody)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

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
        {currentPosts.map((message) => (
          <div
            key={message.id}
            className="col-sm-6 mb-3 mb-sm-3"
            onMouseEnter={() => setHoveredMessageId(message.id)}
            onMouseLeave={() => setHoveredMessageId(null)}
          >
            <a
              href={"https://t.me/" + channelUsername + "/" + message.id}
              target="_blank"
              className="card-link position-relative"
            >
              <div className="card h-100 w-100">
                <div className="card-body snscrape text-center">
                  <h6 className="card-subtitle mb-2 text-body-secondary">
                    {message.user.username
                      ? "@" + message.user.username
                      : message.user.first_name +
                        (message.user.last_name != null
                          ? " " + message.user.last_name
                          : "")}
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
                {hoveredMessageId === message.id && (
                  <>
                    {message.user.username && (
                      <div className="card-footer">
                        <button
                          className="btn btn-primary btn-sm"
                          onClick={(event) => {
                            event.preventDefault();
                            handleUsernameAnalysisClick(
                              message.user.username || ""
                            );
                          }}
                        >
                          Username analysis
                        </button>
                      </div>
                    )}
                  </>
                )}
                <MdOpenInNew className="position-absolute top-0 end-0 mt-2 me-2 invisible" />
              </div>
            </a>
          </div>
        ))}
      </div>
      <nav>
        <ul className="pagination justify-content-center mt-2">
          <li className={`page-item ${currentPage === 1 ? "disabled" : ""}`}>
            <button
              className="page-link me-2"
              onClick={() => paginate(currentPage - 1)}
            >
              Previous
            </button>
          </li>
          {Array(Math.ceil(filteredPosts.length / postsPerPage))
            .fill(0)
            .map((_, index) => (
              <li
                key={index}
                className={`page-item ms-1 me-1 ${
                  currentPage === index + 1 ? "active" : ""
                }`}
              >
                <button
                  className="page-link"
                  onClick={() => paginate(index + 1)}
                >
                  {index + 1}
                </button>
              </li>
            ))}
          <li
            className={`page-item ${
              currentPage === totalPages ? "disabled" : ""
            }`}
          >
            <button
              className="page-link ms-2"
              onClick={() => paginate(currentPage + 1)}
            >
              Next
            </button>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default TelegramTrackerResults;
