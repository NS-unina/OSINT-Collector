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
  return (
    <div>
      <div
        className="mb-3"
        id="sernameContainer"
        style={{ maxHeight: "400px", overflowY: "scroll" }}
      >
        <label className="form-label">Usernames:</label>
        {usernames.map((username) => (
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
