import {React, useState} from 'react';

const Look = () => {
  const [selectedCategories, setSelectedCategories] = useState([]);
  const categories = ['Durability', 'Cool', 'Price', 'Saved Marriage', 'Ease of Use'];

  const reviews = [
    {
      text: "This product saved my marriage. Before this product my life is in shambles but ever since I bought this product my wife respects me. Thank you company who made this product.",
      rating: 5,
      author: "Satisfied Customer"
    },
    {
      text: "This product is so great and cool and very good I love this product.",
      rating: 5,
      author: "Satisfied Customer"
    },
    {
      text: "This product is so great and cool and very good I love this product.",
      rating: 5,
      author: "Satisfied Customer"
    },
    {
      text: "This product saved my marriage. Before this product my life is in shambles but ever since I bought this product my wife respects me. Thank you company who made this product.",
      rating: 5,
      author: "Satisfied Customer"
    }
  ];

  const toggleCategory = (category) => {
    setSelectedCategories((prev) =>
      prev.includes(category)
        ? prev.filter((cat) => cat !== category) // Deselect
        : [...prev, category] // Select
    );
  };


  return (
    <div className="bg-red-500 p-4 rounded-lg w-full max-w-xl">
          <div className="mb-4">
            <h3 className="text-lg font-bold text-white mb-2">Categories:</h3>
            <div className="flex flex-wrap gap-2">
              {categories.map((category, index) => (
                <span key={index} 
                onClick={() => toggleCategory(category)}
                className={`px-3 py-1 rounded-full text-sm cursor-pointer 
                  ${selectedCategories.includes(category) ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}`}
    >
                  {category}
                </span>
              ))}
            </div>
          </div>
          <div className="space-y-3 overflow-y-auto" style={{ maxHeight: '300px' }}>
            {reviews.map((review, index) => {
              return (
                <div key={index} className="bg-gray-100 p-3 rounded-lg">
                  <p className="text-sm mb-2">{review.text}</p>
                  <div className="flex justify-between items-center text-xs text-gray-600">
                    <span>({review.rating} stars)</span>
                    <span>-{review.author}</span>
                  </div>
                </div>
              );
            })}
      </div>
    </div>
  );
};

export default Look;

