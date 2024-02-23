import { useEffect, useRef, useState } from "react";
import { InstagramAccount } from "../types/results";
import axios from "axios";
import { FaTimes } from "react-icons/fa";

interface Props {
  id: number;
  title: string;
  tags: string[];
  endpoint: string;
  onSendRequest: (endpoint: string, input: string[]) => void;
  handleCloseInput: () => void;
  handleCloseCard: () => void;
  setSelectedCard: (id: number) => void;
}

const UsernameInferenceCard = ({
  id,
  title,
  tags,
  endpoint,
  onSendRequest,
  handleCloseInput,
  handleCloseCard,
  setSelectedCard,
}: Props) => {
  const [inputVisible, setInputVisible] = useState(false);
  const [inputValues, setInputValues] = useState<string[]>(
    new Array(tags.length).fill("")
  );
  const [selectedInputs, setSelectedInputs] = useState<string[]>(
    new Array(tags.length).fill("")
  );
  const [selected, setSelected] = useState(false);
  const [usernames, setusernames] = useState<InstagramAccount[]>([]);
  const [suggestedusernames, setSuggestedusernames] = useState<
    InstagramAccount[]
  >([]);
  const inputRefs = useRef<(HTMLInputElement | null)[]>(
    new Array(tags.length).fill(null)
  );

  const fetchusernames = () => {
    axios
      .get<InstagramAccount[]>(`http://localhost:8080/` + endpoint)
      .then((res) => setusernames(res.data))
      .catch((error) => console.error("Error fetching data:", error));
  };

  useEffect(() => {
    if (inputVisible && inputRefs.current[0]) {
      inputRefs.current[0]?.focus();
    }
  }, [inputVisible]);

  useEffect(() => {
    if (inputVisible && inputValues.some((value) => value.trim() !== "")) {
      const similarusernames = usernames
        .filter((account) =>
          account.username.toLowerCase().includes(inputValues[0].toLowerCase())
        )
        .sort((a, b) => a.username.localeCompare(b.username))
        .slice(0, 5);
      setSuggestedusernames(similarusernames);
    } else {
      setSuggestedusernames([]);
    }
  }, [inputValues, inputVisible, usernames]);

  const handleCardClick = () => {
    if (!selected) {
      fetchusernames();
      setInputVisible(true);
      setSelected(true);
      setSelectedCard(id);
    }
  };

  const handleInputChange = (
    event: React.ChangeEvent<HTMLInputElement>,
    index: number
  ) => {
    const newInputValues = [...inputValues];
    newInputValues[index] = event.target.value;
    setInputValues(newInputValues);
  };

  const handleBadgeClick = (account: InstagramAccount, index: number) => {
    onSendRequest(tags[index], [account.username]);
    const newSelectedInputs = [...selectedInputs];
    newSelectedInputs[index] = account.username;
    setSelectedInputs(newSelectedInputs);
    const newInputValues = [...inputValues];
    newInputValues[index] = account.username;
    setInputValues(newInputValues);
    setInputVisible(false);
  };

  const handleInstagramAccountClose = () => {
    setInputVisible(true);
    setSelectedInputs(new Array(tags.length).fill(""));
    setInputValues(new Array(tags.length).fill(""));
    handleCloseInput();
  };

  const handleCardClose = () => {
    handleCloseCard();
    setInputVisible(false);
    setSelectedInputs(new Array(tags.length).fill(""));
    setSelected(false);
  };

  const renderTitleWithTags = () => {
    let updatedTitle = title;
    tags.forEach((tag, index) => {
      updatedTitle = updatedTitle.replace(
        `[${tag}]`,
        `<div class="badge bg-primary me-1 mb-1">${
          selectedInputs[index] === "" ? tag : selectedInputs[index]
        }</div>`
      );
    });
    return <div dangerouslySetInnerHTML={{ __html: updatedTitle }} />;
  };

  return (
    <div className="col-sm-4 mt-3">
      <div
        className={`card h-100 w-100 ${selected ? "selected" : ""}`}
        onClick={handleCardClick}
      >
        <div className="card-body snscrape">
          {inputVisible && (
            <div
              onClick={handleCardClose}
              className="position-absolute top-0 start-100 translate-middle mt-1"
            >
              <div className="icon-wrapper">
                <FaTimes className="icon-red" />
              </div>
            </div>
          )}
          <div className="card-text">
            {renderTitleWithTags()}
            {inputVisible && (
              <div>
                {tags.map((tag, index) => (
                  <div key={index}>
                    <input
                      ref={(el) => (inputRefs.current[index] = el)}
                      type="text"
                      className="form-control border border-2 border-primary mt-3"
                      placeholder={tag}
                      value={inputValues[index]}
                      onChange={(event) => handleInputChange(event, index)}
                      autoFocus={index === 0}
                    />
                    <div className="suggested-usernames d-flex flex-wrap mt-3">
                      {suggestedusernames.map((account) => (
                        <div
                          key={account.id}
                          className="badge bg-primary me-1 mb-1"
                          onClick={() => handleBadgeClick(account, index)}
                        >
                          {account.username}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
          {selectedInputs.some((input) => input !== "") && (
            <div
              onClick={handleInstagramAccountClose}
              className="position-absolute top-0 start-100 translate-middle mt-1"
            >
              <div className="icon-wrapper">
                <FaTimes className="icon-red" />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UsernameInferenceCard;
