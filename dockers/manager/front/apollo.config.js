module.exports = {
  client: {
    service: {
      name: "pwn-machine",
      // URL to the GraphQL API
      url: "http://127.0.0.1:8000/api"
    },
    // Files processed by the extension
    includes: ["src/**/*.vue", "src/**/*.js", "src/**/*.graphql"]
  }
};
