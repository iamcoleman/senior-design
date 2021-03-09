module.exports = (scores) => {
    const count = scores.length;
    if(count === 0) {
        return {
            count: 0
        };
    }

    let averageScore = 0;
    for(const score of scores) {
        averageScore += score;
    }
    averageScore /= count;

    let lowTotal = 0;
    let lowCount = 0;
    let highTotal = 0;
    let highCount = 0;
    for(const score of scores) {
        if(score < averageScore) {
            lowTotal += score;
            lowCount++;
        } else if(score > averageScore) {
            highTotal += score;
            highCount++;
        }
    }
    
    return {
        score: averageScore,
        count: count,
        lowAverage: lowCount === 0 ? averageScore : lowTotal / lowCount / 2 + averageScore / 2,
        highAverage: highCount === 0 ? averageScore : highTotal / highCount / 2 + averageScore / 2
    };
}
