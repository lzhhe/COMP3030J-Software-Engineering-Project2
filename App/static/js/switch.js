$(document).ready(function () {
// 一开始就检查存储的主题和语言设置
    const theme = $('#themeSwitch input');
    const language = $('#languageSwitch input');
    const html = $('html');
    if (localStorage.getItem('theme') === 'dark') {
        html.attr('data-theme', 'dark');
        theme.prop('checked', true);// 监听主题切换的点击事件
    }
    if (localStorage.getItem('language') === 'zh') {
        html.attr('lang', 'en');
        language.prop('checked', true);
    }


    theme.change(function () {
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
        if (html.attr('lang') === 'en') {
            html.attr('lang', 'zh');
            localStorage.setItem('language', 'zh');
        } else {
            html.attr('lang', 'en');
            localStorage.setItem('language', 'en');
            // 类似地，处理语言切换回英文的逻辑
        }
    });
});
