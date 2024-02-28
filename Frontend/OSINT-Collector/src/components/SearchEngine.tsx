import axios from "axios";
import { GoogleSearchResponse } from "../types";
import { useEffect, useState } from "react";
import SearchResults from "./SearchResults";
import AlertMessage from "./AlertMessage";

const SearchEngine = () => {
  const [searchValue, setSearchValue] = useState("");
  const [searchResults, setSearchResults] =
    useState<GoogleSearchResponse | null>(null);
  const [pageSearchResults, setPageSearchResults] = useState(0);

  useEffect(() => {
    handleSearchEngineSubmit();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pageSearchResults]);

  const handleSearchEngineSubmit = () => {
    if (searchValue) {
      axios
        .get(
          "http://localhost:8080/proxy?param=" +
            searchValue +
            "&page=" +
            pageSearchResults
        )
        .then((response) => {
          setSearchResults(response.data);
        })
        .catch((error) => {
          console.error("Error fetching search results:", error);
        });
    }
  };

  return (
    <>
      <div className="mb-1">
        <label className="form-label">Telegram Search Engine:</label>
      </div>
      <div className="input-group mb-3">
        {searchResults !== null && !searchResults?.error && (
          <button
            className="btn btn-outline-danger"
            type="button"
            id="button-addon2"
            onClick={() => {
              setSearchValue("");
              setSearchResults(null);
            }}
          >
            Clear
          </button>
        )}
        <input
          id="searchInput"
          type="text"
          className="form-control"
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          placeholder="Search for Channels, Bots & Groups"
        />
        <button
          className="btn btn-outline-info"
          type="button"
          id="button-addon2"
          onClick={handleSearchEngineSubmit}
        >
          Search
        </button>
      </div>
      {searchResults != null && !searchResults?.error && (
        <div>
          <SearchResults
            searchResponse={searchResults}
            onPageChange={(page) => {
              setPageSearchResults((page - 1) * 10);
            }}
          />
        </div>
      )}
      {searchResults != null && searchResults?.error && (
        <div>
          <AlertMessage
            message={"Change IP address - " + searchResults?.error.message}
            onClose={() => {
              setSearchValue("");
              setSearchResults(null);
            }}
            type="danger"
          />
        </div>
      )}
    </>
  );
};

export default SearchEngine;
