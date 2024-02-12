import { useEffect, useState } from "react";
import axios from "axios";
import { Launch } from "../types";
import { blackbird, instaloader, snscrape } from "../types/results";
import BlackbirdResults from "./BlackbirdResults";
import SnscrapeResults from "./SnscrapeResults";

interface Props {
  selectedLaunch: Launch | null;
}

const ShowResults = ({ selectedLaunch }: Props) => {
  const [results, setResults] = useState(() => {
    switch (selectedLaunch?.image) {
      case "blackbird":
        return {} as blackbird;
      case "snscrape-telegram":
        return {} as snscrape;
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
          .post<blackbird | instaloader | snscrape>(
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
        return <BlackbirdResults results={results} />;
      }
      break;
    case "snscrape-telegram":
      if (results !== null && "posts" in results && "name" in results) {
        return (
          <SnscrapeResults
            results={results}
            filter={parseInt(selectedLaunch.inputs[1])}
          />
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
