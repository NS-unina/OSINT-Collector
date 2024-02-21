import { useEffect, useRef, useState } from "react";
import { Category } from "../types/results";
import axios from "axios";
import { FaTimes } from "react-icons/fa";

interface Props {
  title: string;
  tag: string;
  endpoint: string;
  onSendRequest: (endpoint: string, input: string) => void;
  handleClose: () => void;
}

const InferenceCard = ({
  title,
  tag,
  endpoint,
  onSendRequest,
  handleClose,
}: Props) => {
  const [inputVisible, setInputVisible] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selected, setSelected] = useState(false);
  const [categories, setCategories] = useState<Category[]>([]);
  const [suggestedCategories, setSuggestedCategories] = useState<Category[]>(
    []
  );
  const inputRef = useRef<HTMLInputElement>(null);

  const fetchCategories = () => {
    axios
      .get<Category[]>(`http://localhost:8080/` + endpoint)
      .then((res) => setCategories(res.data))
      .catch((error) => console.error("Error fetching data:", error));
  };

  useEffect(() => {
    if (inputVisible && inputRef.current) {
      inputRef.current.focus();
    }
  }, [inputVisible]);

  useEffect(() => {
    if (inputVisible && inputValue.trim() !== "") {
      const similarCategories = categories
        .filter((category) =>
          category.name.toLowerCase().includes(inputValue.toLowerCase())
        )
        .sort((a, b) => a.name.localeCompare(b.name))
        .slice(0, 5);
      setSuggestedCategories(similarCategories);
    } else {
      setSuggestedCategories([]);
    }
  }, [inputValue, inputVisible, categories]);

  const handleCardClick = () => {
    if (!selected) {
      fetchCategories();
      setInputVisible(true);
      setSelected(true);
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const handleBadgeClick = (category: Category) => {
    onSendRequest(tag, category.name);
    setInputValue(category.name);
    setInputVisible(false);
    setSelectedCategory(category.name);
  };

  const handleCategoryClose = () => {
    setInputVisible(true);
    setSelectedCategory("");
    handleClose();
  };

  return (
    <div className="col-sm-4 mt-3">
      <div
        className={`card h-100 w-100 ${selected ? "selected" : ""}`}
        onClick={handleCardClick}
      >
        <div className="card-body snscrape">
          <div className="card-text">
            {title}
            {inputVisible ? (
              <div>
                <input
                  ref={inputRef}
                  type="text"
                  className="form-control border border-2 border-primary mt-3"
                  placeholder={tag}
                  value={inputValue}
                  onChange={handleInputChange}
                  autoFocus
                />
                <div className="suggested-categories d-flex flex-wrap mt-3">
                  {suggestedCategories.map((category) => (
                    <div
                      key={category.uri}
                      className="badge bg-primary me-1 mb-1"
                      onClick={() => handleBadgeClick(category)}
                    >
                      {category.name}
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="badge bg-primary me-1 mb-1">
                {selectedCategory == "" ? tag : selectedCategory}
              </div>
            )}
          </div>
          {selectedCategory && (
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
