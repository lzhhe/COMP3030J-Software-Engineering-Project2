$(document).ready(function () {
    const themeButton = $('#themeSwitch input');
    const languageButton = $('#languageSwitch input');
    const html = $('html');
    updateIconsTheme();
    if (html.attr('data-theme') === 'dark') {
        themeButton.prop('checked', true);
    }

    if (html.attr('lang') === 'zh_Hans_CN') {
        languageButton.prop('checked', true);
    }


    // 监听主题切换的点击事件
    themeButton.change(function () {
        const theme = themeButton.is(':checked') ? 'dark' : 'light';
        $.post(themeUrl, {theme: theme}, function () {
            html.attr('data-theme', theme);
            updateIconsTheme();
        });
    });

    // 监听语言切换的点击事件
    languageButton.change(function () {
        const language = languageButton.is(':checked') ? 'zh_Hans_CN' : 'en';
        $.post(langUrl, {language: language}, function () {
            html.attr('lang', language);
            location.reload();
        });
    });

    // 当文档加载完毕时运行

    function updateIconsTheme() {
        // 检查data-theme属性的值
        if (html.attr('data-theme') === 'dark') {
            $('.icons').addClass('icon-dark');
        } else {
            $('.icons').removeClass('icon-dark');
        }
    }
});
