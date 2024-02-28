import { useEffect, useRef, useState } from "react";
import { Category } from "../types/results";
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

const InferenceCard = ({
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
  const [categories, setCategories] = useState<Category[]>([]);
  const [suggestedCategories, setSuggestedCategories] = useState<Category[]>(
    []
  );
  const inputRefs = useRef<(HTMLInputElement | null)[]>(
    new Array(tags.length).fill(null)
  );

  const fetchCategories = () => {
    axios
      .get<Category[]>(`http://localhost:8080/` + endpoint)
      .then((res) => setCategories(res.data))
      .catch((error) => console.error("Error fetching data:", error));
  };

  useEffect(() => {
    if (inputVisible && inputRefs.current[0]) {
      inputRefs.current[0]?.focus();
    }
  }, [inputVisible]);

  useEffect(() => {
    if (inputVisible && inputValues.some((value) => value.trim() !== "")) {
      const similarCategories = categories
        .filter((category) =>
          category.name.toLowerCase().includes(inputValues[0].toLowerCase())
        )
        .sort((a, b) => a.name.localeCompare(b.name))
        .slice(0, 5);
      setSuggestedCategories(similarCategories);
    } else {
      setSuggestedCategories([]);
    }
  }, [inputValues, inputVisible, categories]);

  const handleCardClick = () => {
    if (!selected) {
      fetchCategories();
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

  const handleBadgeClick = (category: Category, index: number) => {
    onSendRequest(tags[index], [category.name]);
    const newSelectedInputs = [...selectedInputs];
    newSelectedInputs[index] = category.name;
    setSelectedInputs(newSelectedInputs);
    const newInputValues = [...inputValues];
    newInputValues[index] = category.name;
    setInputValues(newInputValues);
    setInputVisible(false);
  };

  const handleCategoryClose = () => {
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
        `<div class="badge bg-warning me-1 mb-1">${
          selectedInputs[index] === "" ? tag : selectedInputs[index]
        }</div>`
      );
    });
    return <div dangerouslySetInnerHTML={{ __html: updatedTitle }} />;
  };

  return (
    <div className={`col-sm-4 mt-3`} style={selected ? { width: "500px" } : {}}>
      <div
        className={`card h-100 w-100 ${
          selected ? "selected border border-warning" : ""
        }`}
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
                      className="form-control border border-2 border-warning mt-3"
                      placeholder={tag}
                      value={inputValues[index]}
                      onChange={(event) => handleInputChange(event, index)}
                      autoFocus={index === 0}
                    />
                    <div className="suggested-categories d-flex flex-wrap mt-3">
                      {suggestedCategories.map((category) => (
                        <div
                          key={category.uri}
                          className="badge bg-warning me-1 mb-1"
                          onClick={() => handleBadgeClick(category, index)}
                        >
                          {category.name}
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
              onClick={handleCategoryClose}
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

export default InferenceCard;
