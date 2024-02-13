import { useState } from "react";
import { instaloader } from "../types/results";
import { MdOpenInNew, MdPersonAdd } from "react-icons/md";
import { MdFavorite, MdMessage } from "react-icons/md";
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

  return (
    <div>
      <div className="d-flex justify-content-center mb-3 mt-3">
        <InstaloaderProfileInfo {...results} />
      </div>
      <div className="d-flex justify-content-center align-items-center mb-3">
        <button
          className="btn btn-primary mx-2"
          onClick={() => setShowAll(true)}
        >
          All posts
        </button>
        <button
          className="btn btn-danger mx-2"
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
                <div className="card-body snscrape">
                  <h5 className="card-title">{results.username}</h5>
                  <p className="card-text">{post.text}</p>
                  <div className="d-flex flex-wrap align-items-center">
                    <div className="me-2">
                      <MdFavorite /> {post.likes} Likes
                    </div>
                    <div>
                      <MdMessage /> {post.comments} Comments
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
