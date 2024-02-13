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
  return (
    <div>
      <div
        className="mb-3"
        id="instagramAccountsContainer"
        style={{ maxHeight: "400px", overflowY: "scroll" }}
      >
        <label className="form-label">Instagram Accounts:</label>
        {accounts.map((account) => (
          <div key={account.id} className="mb-2">
            <input
              type="checkbox"
              className="btn-check"
              id={`telegram-${account.id}`}
              value={account.username}
              autoComplete="off"
              checked={selectedAccount?.id === account.id}
              onChange={() => handleAccountToggle(account.id)}
            />
            <label
              className="btn btn-outline-success tool-label"
              htmlFor={`telegram-${account.id}`}
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
