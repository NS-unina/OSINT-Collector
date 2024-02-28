import { blackbird } from "../types/results";
import { MdOpenInNew } from "react-icons/md";

interface Props {
  results: blackbird;
  instaRef: (username: string) => void;
}

const blacklist = [
  "BugBounty",
  "Independent academia",
  "Academia.edu",
  "Xhamster",
  "TryHackMe",
  "HackenProof",
];

const BlackbirdResults = ({ results, instaRef }: Props) => {
  return (
    <div>
      <div className="row mt-5">
        {results.sites
          .filter((site) => site.status === "FOUND")
          .filter((site) => {
            return !blacklist.some((word) =>
              site.site.toLowerCase().includes(word.toLowerCase())
            );
          })
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
                    {site.site == "Instagram" ? (
                      <a
                        onClick={(event) => {
                          event.preventDefault();
                          instaRef(results.username);
                        }}
                        className="btn btn-primary"
                      >
                        ANALYZED
                      </a>
                    ) : (
                      <></>
                    )}
                  </div>
                  <MdOpenInNew className="position-absolute top-0 end-0 mt-2 me-2 invisible" />
                </div>
              </a>
            </div>
          ))}
      </div>
    </div>
  );
};

export default BlackbirdResults;
