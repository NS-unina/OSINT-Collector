import { useState } from "react";
import { FaSortAlphaDown, FaSortAlphaUpAlt } from "react-icons/fa";
import { instaloader } from "../types/results";

interface Props {
  accounts: instaloader[];
  selectedAccount: instaloader | null;
  handleAccountToggle: (accountId: string) => void;
}

const InstagramAccountList = ({
  accounts,
  selectedAccount,
  handleAccountToggle,
}: Props) => {
  const [ascending, setAscending] = useState(true);

  const sortedAccounts = [...accounts].sort((a, b) => {
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
        id="instagramAccountsContainer"
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
            <div>Instagram Accounts:</div>
          </label>
        </div>
        {sortedAccounts.map((account) => (
          <div key={account.id} className="mb-2">
            <input
              type="checkbox"
              className="btn-check"
              id={`instagram-${account.id}`}
              value={account.username}
              autoComplete="off"
              checked={selectedAccount?.id === account.id}
              onChange={() => handleAccountToggle(account.id)}
            />
            <label
              className="btn btn-outline-success tool-label"
              htmlFor={`instagram-${account.id}`}
            >
              {account.username}
            </label>
          </div>
        ))}
      </div>
    </div>
  );
};

export default InstagramAccountList;
