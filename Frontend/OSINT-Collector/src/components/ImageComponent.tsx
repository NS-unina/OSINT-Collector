import { useState, useEffect } from "react";
import axios from "axios";

interface Props {
  imageUrl: string;
  size: string;
}

const ImageComponent = ({ imageUrl, size }: Props) => {
  const [imageData, setImageData] = useState<string | null>(null);

  useEffect(() => {
    const fetchImage = async () => {
      try {
        const response = await axios.get("http://localhost:8080/proxy-image", {
          params: { url: imageUrl },
          responseType: "blob",
        });
        setImageData(URL.createObjectURL(response.data));
      } catch (error) {
        console.error("Error fetching image:", error);
      }
    };

    if (imageUrl) {
      fetchImage();
    }
  }, [imageUrl]);

  return imageData ? (
    <div style={{ width: size || "auto", height: size || "auto" }}>
      <img
        src={imageData}
        className="card-img-top img-fluid"
        alt="Instagram"
        style={{ width: "100%", height: "100%", objectFit: "cover" }}
      />
    </div>
  ) : (
    <div>Loading...</div>
  );
};

export default ImageComponent;
