import React, { useState, useEffect } from 'react';
import { ChevronDown} from 'lucide-react';
import Look from './components/lookAtReviews'
import Make from './components/makeReview.js'


const Widget = () => {
  const [activeOption, setActiveOption] = useState(null);
  const [url, setUrl] = useState('');
  
  useEffect(() => {
    const currentUrl = window.location.href;
    setUrl(currentUrl);
    const postUrl = async () => {
      const urlData = {
        url: url
      };

      try {
        const response = await fetch('http://localhost:5000/process/product', {
          method: 'POST',
          body: urlData
        });
        const data = await response.json();
                if (response.ok) {
                    console.log('URL added:', data);
                } else {
                    console.error('Error adding URL:', data);
                }
      } catch (error) {
          console.error('Network error:', error);
      }
      
    };

    postUrl(); // Call the function to post data
  }, [url]);


  const toggleOption = (option) => {
    setActiveOption(activeOption === option ? null : option);
  };

  

  return (
    <div className="flex flex-col items-center p-4 bg-gray-800 rounded-lg">
      <div className="flex space-x-4 mb-4">
        <button
          onClick={() => toggleOption('leave')}
          className="flex items-center justify-between px-4 py-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
        >
          Leave a Review
          <ChevronDown className={`ml-2 transition-transform ${activeOption === 'leave' ? 'rotate-180' : ''}`} />
        </button>
        <button
          onClick={() => toggleOption('look')}
          className="flex items-center justify-between px-4 py-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
        >
          Look at Reviews
          <ChevronDown className={`ml-2 transition-transform ${activeOption === 'look' ? 'rotate-180' : ''}`} />
        </button>
      </div>
      
      {activeOption === 'leave' && <Make />}
      
      {activeOption === 'look' && <Look />}
    </div>
  );
};

export default Widget;