import React, { useState } from 'react';
import './TagDisplay.css';

function TagDisplay(props) {
  const [showMore, setShowMore] = useState(false);

  let { hashtags } = props;
  if(!showMore) {
    hashtags = hashtags.slice(0, 5);
  }

  return (
    <p className="tagDisplay">Related hashtags:{' '}
      {
        hashtags.length === 0 ? 'None' : hashtags
          .map((tag, i) => <>
            <button onClick={() => props.searchTag(tag)}>#{tag}</button>,{' '}
          </>)
      }
      {
        props.hashtags.length > 5 &&
          <button onClick={() => setShowMore(!showMore)}>...show {showMore ? 'less' : 'more'}</button>
      }
    </p>
  );
}

export default TagDisplay;
