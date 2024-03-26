$(document).ready(function () {
    const themeButton = $('#themeSwitch input');
    const languageButton = $('#languageSwitch input');
    const html = $('html');

    // 一开始就检查存储的主题设置
    if (localStorage.getItem('theme') === 'dark') {
        html.attr('data-theme', 'dark');
        themeButton.prop('checked', true);
    }

    // 一开始就检查存储的语言设置
    if (localStorage.getItem('language') === 'zh') {
        html.attr('lang', 'zh'); // 注意这里应当是 'zh'
        languageButton.prop('checked', true);
    }

    // 监听主题切换的点击事件
    themeButton.change(function () {
        if (themeButton.is(':checked')) {
            html.attr('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            html.attr('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });

    // 监听语言切换的点击事件
    languageButton.change(function () {
        if (languageButton.is(':checked')) {
            html.attr('lang', 'zh');
            localStorage.setItem('language', 'zh');
        } else {
            html.attr('lang', 'en');
            localStorage.setItem('language', 'en');
        }
    });
});
