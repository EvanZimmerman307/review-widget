import React, {useState} from 'react';
import { Star} from 'lucide-react';
const Make = () => {
  const [rating, setRating] = useState(5);
  const [review, setReview] = useState('');
  const [email, setEmail] = useState('');
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log({ rating, review, email });
    // Here you would typically send this data to your backend
  };

  return (<div className="bg-red-500 p-6 rounded-lg w-full max-w-md">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <p className="text-white mb-2">RATING :</p>
              <div className="flex justify-center bg-white rounded-full p-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <Star
                    key={star}
                    size={24}
                    className={`cursor-pointer ${star <= rating ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'}`}
                    onClick={() => setRating(star)}
                  />
                ))}
              </div>
            </div>
            <input
              type="text"
              className="w-full p-3 rounded-full"
              placeholder="How did this product impact your life?"
            />
            <div>
              <p className="text-white mb-2">REVIEW :</p>
              <textarea
                className="w-full p-3 rounded-3xl"
                rows="4"
                value={review}
                onChange={(e) => setReview(e.target.value)}
                placeholder="Write your review here..."
              ></textarea>
            </div>
            <div>
              <p className="text-white mb-2">EMAIL:</p>
              <input
                type="email"
                className="w-full p-3 rounded-full"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
              />
            </div>
            <button
              type="submit"
              className="px-6 py-2 bg-gray-400 text-white rounded-full hover:bg-gray-500 transition-colors float-right"
            >
              SUBMIT
            </button>
          </form>
        </div>);
};

export default Make;