module.exports = {
    darkMode: 'class',
    content: [
        './**/*.html',
        './node_modules/flowbite/**/*.js',
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('flowbite/plugin'),
    ],
}