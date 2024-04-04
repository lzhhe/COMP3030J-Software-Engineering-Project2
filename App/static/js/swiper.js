$(document).ready(function () {
    const swiper = new Swiper('.swiper', {
        loop: true,
        autoplay: {
            delay: 2500, // 每个滑块停留 2500 毫秒
            disableOnInteraction: false, // 用户操作swiper之后，是否禁止autoplay。默认为true：停止。
        },
        spaceBetween: 30,
        speed: 1000,
        grabCursor: true,
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            dynamicBullets: true,
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        breakpoints: {
            800: {
                slidesPerView: 1,
            },
            1000: {
                slidesPerView: 2,
            },
            1200: {
                slidesPerView: 3,
            },
        },
    });
});

