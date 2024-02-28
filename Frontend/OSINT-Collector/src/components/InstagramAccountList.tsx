import { useState } from "react";
import { FaSortAlphaDown, FaSortAlphaUpAlt, FaTimes } from "react-icons/fa";
import { instaloader } from "../types/results";
import { GoAlertFill } from "react-icons/go";
import Switch from "./Switch";

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
  const [showAll, setShowAll] = useState(true);

  const sortedAccounts = [...accounts].sort((a, b) => {
    if (ascending) {
      return a.username.localeCompare(b.username);
    } else {
      return b.username.localeCompare(a.username);
    }
  });

  const filteredAccounts = showAll
    ? sortedAccounts
    : accounts.filter((account) => account.flag);

  return (
    <div>
      <div
        className="mb-3"
        id="instagramAccountsContainer"
        style={{ maxHeight: "500px", overflowY: "scroll" }}
      >
        <div className="d-flex justify-content-center align-items-center mb-2">
          <label className="form-label d-flex align-items-center">
            {selectedAccount == null && (
              <Switch
                isOn={!showAll}
                type="alert"
                color="#f44336"
                handleToggle={() => {
                  setShowAll(!showAll);
                }}
              />
            )}
            <div
              className="ms-2 pe-2 btn-link"
              onClick={(event) => {
                event.preventDefault();
                setAscending(!ascending);
              }}
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
        {filteredAccounts.map((account) => (
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
              className={`btn btn-outline-success tool-label ${
                account.username === selectedAccount?.username || account.flag
                  ? "position-relative"
                  : ""
              }`}
              htmlFor={`instagram-${account.id}`}
            >
              {account.username}
              {account.username === selectedAccount?.username && (
                <div className="position-absolute top-0 start-100 translate-middle mt-1">
                  <div className="icon-wrapper">
                    <FaTimes className="icon-red" />
                  </div>
                </div>
              )}
              {account.flag && (
                <div className="position-absolute top-50 start-0 translate-middle ms-1">
                  <div className="icon-wrapper">
                    <GoAlertFill className="icon-red mb-1" />
                  </div>
                </div>
              )}
            </label>
          </div>
        ))}
      </div>
    </div>
  );
};

export default InstagramAccountList;
