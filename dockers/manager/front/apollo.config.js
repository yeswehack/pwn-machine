
module.exports = {
    client: {
        service: {
            name: 'my-app',
            // URL to the GraphQL API
            url: '/api',
        },
        // Files processed by the extension
        includes: [
            'src/**/*.vue',
            'src/**/*.js',
        ],
    },
}