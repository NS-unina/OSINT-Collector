import { useState } from "react";
import { TelegramChannel } from "../types/results";
import { GoAlertFill } from "react-icons/go";
import { FaSortAlphaDown, FaSortAlphaUpAlt, FaTimes } from "react-icons/fa";
import Switch from "./Switch";

interface Props {
  accounts: TelegramChannel[];
  selectedChannel: TelegramChannel | null;
  handleChannelToggle: (channelName: string) => void;
}

const TelegramChannelList = ({
  accounts,
  selectedChannel,
  handleChannelToggle,
}: Props) => {
  const [ascending, setAscending] = useState(true);
  const [showAllChannels, setShowAllChannels] = useState(true);

  const sortedAccounts = [...accounts].sort((a, b) => {
    if (ascending) {
      return a.name.localeCompare(b.name);
    } else {
      return b.name.localeCompare(a.name);
    }
  });

  const handleSetShowAllChannels = () => {
    setShowAllChannels(!showAllChannels);
  };

  const filteredChannels = showAllChannels
    ? sortedAccounts
    : accounts.filter((account) => account.flag);

  return (
    <div>
      <div
        className="mb-3"
        id="telegramAccountsContainer"
        style={{ maxHeight: "400px", overflowY: "scroll" }}
      >
        <div className="d-flex justify-content-center align-items-center mb-2">
          <label className="form-label d-flex align-items-center">
            {selectedChannel == null && (
              <Switch
                isOn={!showAllChannels}
                type="alert"
                color="#f44336"
                handleToggle={handleSetShowAllChannels}
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
            <div>Telegram Channels:</div>
          </label>
        </div>
        {filteredChannels.map((account) => (
          <div key={account.name} className="mb-2">
            <input
              type="checkbox"
              className="btn-check"
              id={`telegram-${account.name}`}
              value={account.name}
              autoComplete="off"
              checked={selectedChannel?.name === account.name}
              onChange={() => handleChannelToggle(account.name)}
            />
            <label
              className={`btn btn-outline-success tool-label ${
                account.name === selectedChannel?.name || account.flag
                  ? "position-relative"
                  : ""
              }`}
              htmlFor={`telegram-${account.name}`}
            >
              <span>{account.name}</span>
              {account.name === selectedChannel?.name && (
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

export default TelegramChannelList;
