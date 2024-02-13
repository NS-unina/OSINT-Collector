import { MdOpenInNew } from "react-icons/md";
import ImageComponent from "./ImageComponent";

interface ProfileInfoProps {
  full_name: string;
  followers: number;
  bio_links: string[];
  biography: string;
  follow: number;
  profile_pic_url: string;
  username: string;
}

const InstaloaderProfileInfo = ({
  full_name,
  followers,
  bio_links,
  biography,
  follow,
  profile_pic_url,
  username,
}: ProfileInfoProps) => {
  return (
    <a
      href={"https://www.instagram.com/" + username}
      target="_blank"
      className="card-link position-relative"
    >
      <div className="card mb-3">
        <div className="card-body" style={{ width: "400px" }}>
          <h5 className="card-title text-center mb-4">Profile</h5>
          <div className="d-flex justify-content-center align-items-center">
            <div
              className="rounded-circle overflow-hidden border border-primary d-flex justify-content-center align-items-center p-1"
              style={{ width: "150px", height: "150px" }}
            >
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  overflow: "hidden",
                  borderRadius: "50%",
                }}
              >
                <ImageComponent imageUrl={profile_pic_url} size={"150px"} />
              </div>
            </div>
          </div>
          <div className="row g-0">
            <div className="h-100 w-100">
              <div className="card-body" style={{ width: "400px" }}>
                <h5 className="card-title">{full_name}</h5>
                <h6 className="card-subtitle mb-4 text-body-secondary">
                  {username}
                </h6>
                <p className="card-text text-left">{biography}</p>
                <div className="d-flex justify-content-center">
                  <p className="card-text mr-2">Followers: {followers}</p>
                  <div style={{ width: "10px" }}></div>{" "}
                  <p className="card-text ml-2">Follow: {follow}</p>
                </div>
                {bio_links && bio_links.length > 0 && (
                  <p className="card-text">
                    Bio Links:
                    <ul>
                      {bio_links.map((link, index) => (
                        <li key={index}>{link}</li>
                      ))}
                    </ul>
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
        <MdOpenInNew className="position-absolute top-0 end-0 mt-2 me-2 invisible" />
      </div>
    </a>
  );
};

export default InstaloaderProfileInfo;
