import { useState } from "react";
import { TelegramChannel } from "../types/results";
import { GoAlertFill } from "react-icons/go";
import { FaSortAlphaDown, FaSortAlphaUpAlt } from "react-icons/fa";

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

  const sortedAccounts = [...accounts].sort((a, b) => {
    if (ascending) {
      return a.name.localeCompare(b.name);
    } else {
      return b.name.localeCompare(a.name);
    }
  });

  return (
    <div>
      <div
        className="mb-3"
        id="telegramAccountsContainer"
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
            <div>Telegram Channels:</div>
          </label>
        </div>
        {sortedAccounts.map((account) => (
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
                account.flag ? "position-relative" : ""
              }`}
              htmlFor={`telegram-${account.name}`}
            >
              <span>{account.name}</span>
              {account.flag && (
                <div className="position-absolute top-50 start-100 translate-middle ms-1">
                  <div className="icon-wrapper">
                    <GoAlertFill className="icon-red" />
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
