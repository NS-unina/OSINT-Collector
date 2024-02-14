import { useState } from "react";
import { FaSortAlphaDown, FaSortAlphaUpAlt } from "react-icons/fa";
import { blackbird } from "../types/results";

interface Props {
  usernames: blackbird[];
  selectedUsername: blackbird | null;
  handleUsernameToggle: (username: string) => void;
}

const UsernameList = ({
  usernames,
  selectedUsername,
  handleUsernameToggle,
}: Props) => {
  const [ascending, setAscending] = useState(true);

  const sortedUsernames = [...usernames].sort((a, b) => {
    if (ascending) {
      return a.username.localeCompare(b.username);
    } else {
      return b.username.localeCompare(a.username);
    }
  });

  return (
    <div>
      <div
        className="mb-3"
        id="sernameContainer"
        style={{ maxHeight: "400px", overflowY: "scroll" }}
      >
        <div className="d-flex justify-content-center align-items-center">
          <label className="form-label d-flex align-items-center">
            <div
              className="pe-2 btn-link"
              onClick={() => setAscending(!ascending)}
            >
              {ascending ? (
                <FaSortAlphaDown type="button" />
              ) : (
                <FaSortAlphaUpAlt type="button" />
              )}
            </div>
            <div>Usernames:</div>
          </label>
        </div>
        {sortedUsernames.map((username) => (
          <div key={username.username} className="mb-2">
            <input
              type="checkbox"
              className="btn-check"
              id={`${username.username}`}
              value={username.username}
              autoComplete="off"
              checked={selectedUsername?.username === username.username}
              onChange={() => handleUsernameToggle(username.username)}
            />
            <label
              className="btn btn-outline-success tool-label"
              htmlFor={`${username.username}`}
            >
              {username.username}
            </label>
          </div>
        ))}
      </div>
    </div>
  );
};

export default UsernameList;
