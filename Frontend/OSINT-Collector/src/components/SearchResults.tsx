import React, { useState } from "react";
import { GoogleSearchResponse } from "../types";

interface Props {
  searchResponse: GoogleSearchResponse;
  onPageChange: (pageNumber: number) => void;
}

const SearchResults: React.FC<Props> = ({ searchResponse, onPageChange }) => {
  const totalResults = parseInt(
    searchResponse.cursor.resultCount.replace(/,/g, "")
  );
  const resultsPerPage = searchResponse.cursor.pages.length;
  const totalPages = Math.ceil(totalResults / resultsPerPage);

  const [currentPage, setCurrentPage] = useState(1);

  const navigateToPage = (pageNumber: number) => {
    setCurrentPage(pageNumber);
    onPageChange(pageNumber);
    window.scrollTo(0, 0);
  };

  const renderPageNumbers = () => {
    const visiblePages = 5; // Number of page numbers to show at a time
    const halfVisiblePages = Math.floor(visiblePages / 2);
    const firstPage = Math.max(1, currentPage - halfVisiblePages);
    const lastPage = Math.min(totalPages, firstPage + visiblePages - 1);

    const pageNumbers = [];
    for (let i = firstPage; i <= lastPage; i++) {
      pageNumbers.push(
        <li
          key={i}
          className={`page-item ${i === currentPage ? "active" : ""}`}
        >
          <button
            className="page-link me-1 ms-1"
            onClick={() => navigateToPage(i)}
          >
            {i}
          </button>
        </li>
      );
    }
    return pageNumbers;
  };

  return (
    <div className="container mt-4">
      <div className="list-group text-start">
        {searchResponse.results.map((result, index) => (
          <a
            key={index}
            href={result.url}
            target="_blank"
            rel="noopener noreferrer"
            className="list-group-item list-group-item-action"
          >
            <div className="d-flex w-100 justify-content-between">
              <h5 className="mb-3">{result.richSnippet.metatags.ogTitle}</h5>
              <small>@{result.breadcrumbUrl.crumbs}</small>
            </div>
            <h6 className="card-subtitle mb-3 text-muted">
              {result.richSnippet.metatags.ogDescription}
            </h6>
            <p className="mb-1">{result.contentNoFormatting}</p>
          </a>
        ))}
      </div>
      <nav aria-label="Search results pagination">
        <ul className="pagination justify-content-center mt-4">
          <li className={`page-item ${currentPage === 1 ? "disabled" : ""}`}>
            <button
              className="page-link me-2"
              onClick={() => navigateToPage(currentPage - 1)}
            >
              Previous
            </button>
          </li>
          {renderPageNumbers()}
          <li
            className={`page-item ${
              currentPage === totalPages ? "disabled" : ""
            }`}
          >
            <button
              className="page-link ms-2"
              onClick={() => navigateToPage(currentPage + 1)}
            >
              Next
            </button>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default SearchResults;
