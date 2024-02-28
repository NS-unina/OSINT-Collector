import { useState } from "react";
import { TelegramGroup } from "../types/results";
import { GoAlertFill } from "react-icons/go";
import { FaSortAlphaDown, FaSortAlphaUpAlt, FaTimes } from "react-icons/fa";
import Switch from "./Switch";

interface Props {
  groups: TelegramGroup[];
  selectedGroup: TelegramGroup | null;
  handleGroupToggle: (groupId: string) => void;
}

const TelegramGroupList = ({
  groups,
  selectedGroup,
  handleGroupToggle,
}: Props) => {
  const [ascending, setAscending] = useState(true);
  const [showAllGroups, setShowAllGroups] = useState(true);

  const sortedAccounts = [...groups].sort((a, b) => {
    if (ascending) {
      return a.username.localeCompare(b.username);
    } else {
      return b.username.localeCompare(a.username);
    }
  });

  const handleSetShowAllGroups = () => {
    setShowAllGroups(!showAllGroups);
  };

  const filteredChannels = showAllGroups
    ? sortedAccounts
    : groups.filter((group) => group.flag);

  return (
    <div>
      <div
        className="mb-3"
        id="telegramAccountsContainer"
        style={{ maxHeight: "400px", overflowY: "scroll" }}
      >
        <div className="d-flex justify-content-center align-items-center mb-2">
          <label className="form-label d-flex align-items-center">
            {selectedGroup == null && (
              <Switch
                isOn={!showAllGroups}
                type="alert"
                color="#f44336"
                handleToggle={handleSetShowAllGroups}
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
            <div>Telegram Groups:</div>
          </label>
        </div>
        {filteredChannels.map((account) => (
          <div key={account.id} className="mb-2">
            <input
              type="checkbox"
              className="btn-check"
              id={`telegram-${account.id}`}
              value={account.id}
              autoComplete="off"
              checked={selectedGroup?.id === account.id}
              onChange={() => handleGroupToggle(account.id)}
            />
            <label
              className={`btn btn-outline-success tool-label ${
                account.id === selectedGroup?.id || account.flag
                  ? "position-relative"
                  : ""
              }`}
              htmlFor={`telegram-${account.id}`}
            >
              <span>{account.username}</span>
              {account.id === selectedGroup?.id && (
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

export default TelegramGroupList;
