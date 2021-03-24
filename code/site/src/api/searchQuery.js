async function getResults(analysisRequestId, resolve, reject) {
    const response = await fetch(`/api/results/${analysisRequestId}`);
    if(!response.ok) {
        reject();
        return;
    }
    const body = await response.json();
    if(body.pending) {
        setTimeout(() => getResults(analysisRequestId, resolve, reject), 10000);
    } else {
        resolve(body);
    }
}

export default async (query) => {
    const analysisStartResponse = await fetch(`/api/sentiment/query/${encodeURIComponent(query)}`, {
        method: 'POST'
    });
    const { analysisRequestId, hashtags } = await analysisStartResponse.json();
    const { scores, dates } = await new Promise((resolve, reject) => getResults(analysisRequestId, resolve, reject));
    if(query.charAt(0) !== '#') {
        delete scores.tumblr;
    }
    return { hashtags, scores, dates };
}
