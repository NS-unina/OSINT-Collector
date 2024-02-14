import { useState } from "react";
import { snscrape } from "../types/results";
import { MdOpenInNew } from "react-icons/md";

interface Props {
  results: snscrape;
  filter?: number;
}

const SnscrapeResults = ({ results, filter }: Props) => {
  const [showAll, setShowAll] = useState(true);

  const sortedPosts = [...results.posts].sort((a, b) => {
    if (a.url < b.url) return 1;
    if (a.url > b.url) return -1;
    return 0;
  });

  const filteredPosts = showAll
    ? sortedPosts
    : sortedPosts.filter((post) => post.processed);

  return (
    <div>
      <div className="d-flex justify-content-center align-items-center mb-4">
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
        {filteredPosts
          .slice(
            0,
            filter != null && filter >= 0 ? filter : filteredPosts.length
          )
          .map((post) => (
            <div key={post.url} className="col-sm-4 mb-3">
              <a
                href={post.url}
                target="_blank"
                className="card-link position-relative"
              >
                <div className="card h-100 w-100">
                  <div className="card-body snscrape text-center">
                    <h5 className="card-title">{results.name}</h5>
                    <p
                      id="cardText"
                      className="card-text p-1"
                      style={{ maxHeight: "300px", overflowY: "scroll" }}
                    >
                      "{post.text}"
                    </p>
                    <div className="d-flex flex-wrap">
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

export default SnscrapeResults;
