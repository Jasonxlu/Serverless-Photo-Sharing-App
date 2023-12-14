// ImageCard.js

import React from "react";
import Image from "next/image";

const ImageCard = ({ src, alt, user, caption, textColor }) => {
  const textStyles = textColor ? `text-${textColor}` : "text-gray-500";

  return (
    <div className={`mt-4 mb-8 w-full ${textStyles}`}>
      {/* User Section */}
      {user && <div className="mb-2 text-sm">{user}</div>}

      {/* Image Section */}
      <div className="relative rounded-md overflow-hidden">
        <Image src={src} alt={alt} width={300} height={150} />
      </div>

      {/* Caption Section */}
      {caption && <div className="mt-2 text-sm">{caption}</div>}
    </div>
  );
};

export default ImageCard;
