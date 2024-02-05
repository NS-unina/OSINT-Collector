import { useEffect, useState } from "react";
import axios from "axios";
import { Launch } from "../types";
import { blackbird, instaloader } from "../types/results";

import { MdOpenInNew } from "react-icons/md";

interface Props {
  selectedLaunch: Launch | null;
}

const ShowResults = ({ selectedLaunch }: Props) => {
  const [results, setResults] = useState(() => {
    switch (selectedLaunch?.image) {
      case "blackbird":
        return {} as blackbird;
      case "instaloader":
        return {} as instaloader;
      default:
        return null;
    }
  });

  useEffect(() => {
    const fetchResults = () => {
      if (selectedLaunch) {
        const formData = {
          image: selectedLaunch?.image,
          inputs: selectedLaunch?.inputs,
        };

        axios
          .post<blackbird | instaloader>(
            "http://localhost:8080/results/" + selectedLaunch?.image,
            formData
          )
          .then((res) => {
            setResults(res.data);
          })
          .catch((error) => {
            console.error("Error fetching response: ", error);
          });
      }
    };

    fetchResults();
  }, [selectedLaunch]);

  if (!selectedLaunch) {
    return <div></div>;
  }

  switch (selectedLaunch.image) {
    case "blackbird":
      if (results !== null && "sites" in results) {
        return (
          <div>
            <div className="row mt-3">
              {results.sites
                .sort((a, b) => a.id - b.id)
                .map((site) => (
                  <div key={site.id} className="col-sm-3 mb-3 mb-sm-3">
                    <a
                      href={site.url}
                      target="_blank"
                      className="card-link position-relative"
                    >
                      <div className="card h-100">
                        <div className="card-body">
                          <h5 className="card-title">{site.site}</h5>
                          <h6 className="card-subtitle mb-2 text-body-secondary">
                            {results.username}
                          </h6>
                        </div>
                        <MdOpenInNew className="position-absolute top-0 end-0 mt-2 me-2 invisible" />
                      </div>
                    </a>
                  </div>
                ))}
            </div>
          </div>
        );
      }
      break;
    case "instaloader":
      // Gestisci i risultati per l'instaloader
      break;
    case "image2":
      return <div></div>;
    default:
      return <div>No results found for this image</div>;
  }
};

export default ShowResults;
