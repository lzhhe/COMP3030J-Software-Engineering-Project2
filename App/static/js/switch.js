$(document).ready(function () {
// 一开始就检查存储的主题和语言设置
    const theme = $('#themeSwitch input');
    const language = $('#languageSwitch input');
// 监听主题切换的点击事件
    theme.change(function () {
        const html = $('html');
        if (html.attr('data-theme') === 'dark') {
            html.attr('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        } else {
            html.attr('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        }
    });

// 监听语言切换的点击事件
    language.change(function () {
        const html = $('html');
        if (savedLanguage === 'en') {
            html.attr('lang', 'zh');
            localStorage.setItem('language', 'zh');
        } else {
            html.attr('lang', 'en');
            localStorage.setItem('language', 'en');
            // 类似地，处理语言切换回英文的逻辑
        }
    });
});
