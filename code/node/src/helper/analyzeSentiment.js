// This is async because it will be an API call
module.exports = async (query) => {
    return Math.floor(Math.random() * 101);
}
