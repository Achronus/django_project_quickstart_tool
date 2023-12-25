if (localStorage.getItem('color-theme') === 'dark' || (
    !('color-theme' in localStorage) &&
    window.matchMedia('(prefers-color-scheme: dark)').matches)
) {
    document.documentElement.classList.add('dark');
} else {
    document.documentElement.classList.remove('dark');
};

// When user explicity chooses light mode
localStorage.theme = 'light';

// When user explicity chooses dark mode
localStorage.theme = 'dark';

// When user chooses to respect OS preferences
localStorage.removeItem('theme');