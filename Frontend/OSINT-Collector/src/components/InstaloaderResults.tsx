import { useState } from "react";
import { instaloader } from "../types/results";
import { MdOpenInNew, MdPersonAdd } from "react-icons/md";
import { MdFavorite, MdMessage } from "react-icons/md";
import { IoCalendar } from "react-icons/io5";
import { FaLocationDot } from "react-icons/fa6";
import InstaloaderProfileInfo from "./InstaloaderProfileInfo";

interface Props {
  results: instaloader;
}

const InstaloaderResults = ({ results }: Props) => {
  const [showAll, setShowAll] = useState(true);

  const sortedPosts = [...results.posts].sort(
    (a, b) => b.timestamp - a.timestamp
  );

  const filteredPosts = showAll
    ? sortedPosts
    : sortedPosts.filter((post) => post.processed);

  const formatDate = (timestamp: number) => {
    const date = new Date(timestamp * 1000);
    return date.toLocaleString(undefined, {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div>
      <div className="d-flex justify-content-center mb-3 mt-3">
        <InstaloaderProfileInfo {...results} />
      </div>
      <div className="d-flex justify-content-center align-items-center mb-3">
        <button
          className={`btn mx-2 ${
            showAll ? "btn-primary" : "btn-outline-primary"
          }`}
          onClick={() => setShowAll(true)}
        >
          All posts
        </button>
        <button
          className={`btn mx-2 ${
            !showAll ? "btn-danger" : "btn-outline-danger"
          }`}
          onClick={() => setShowAll(false)}
        >
          Marked posts
        </button>
      </div>
      <div className="row mt-3">
        {filteredPosts.map((post) => (
          <div key={post.id} className="col-sm-6 mb-3 mb-sm-3">
            <a
              href={"https://www.instagram.com/p/" + post.shortcode}
              target="_blank"
              className="card-link position-relative"
            >
              <div className="card h-100 w-100">
                <div className="card-body snscrape text-center">
                  <h5 className="card-title"></h5>
                  <p className="card-text">"{post.text}"</p>
                  <div className="d-flex flex-wrap align-items-center">
                    <div className="me-2">
                      <MdFavorite /> {post.likes} Likes
                    </div>
                    <div className="me-2">
                      <MdMessage /> {post.comments} Comments
                      <IoCalendar className="ms-3" />{" "}
                      {formatDate(post.timestamp)}
                    </div>
                  </div>
                  {post.taggedAccounts && post.taggedAccounts.length > 0 && (
                    <div className="d-flex flex-wrap mt-2">
                      <MdPersonAdd className="me-1" />
                      {post.taggedAccounts.map((account, index) => (
                        <div
                          key={index}
                          className="badge bg-info me-1 mb-1"
                          role="alert"
                        >
                          @{account}
                        </div>
                      ))}
                    </div>
                  )}
                  {post.location != null && (
                    <div className="d-flex flex-wrap mt-2">
                      <FaLocationDot className="me-1" />
                      <div className="badge bg-success me-1 mb-1" role="alert">
                        {post.location.name}
                      </div>
                    </div>
                  )}
                  {post.categories && post.categories.length > 0 && (
                    <div className="d-flex flex-wrap mt-2">
                      {post.categories.map((category) => (
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

export default InstaloaderResults;
