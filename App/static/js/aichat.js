$(document).ready(function () {
    let open = false;
    const decoder = new TextDecoder();
    const ai_chat_messages = document.getElementById('ai-chat-messages');
    const ai_chat_scroll = document.getElementById('ai-chat-scroll-btn');
    const ai_chat_container = document.getElementById('ai-chat-container');
    const user_input = document.getElementById('ai-chat-user-input');

    const ai_message_init = createMessageBubble('ai-message');
    const init_text = `
hi, I'm the assistant of this waste management web, you can ask me all questions about this system and information of waste types, like:

- **<span class="underline copy-input">What does this system do</span>**
- **<span class="underline copy-input">How do I use this system</span>**
- **<span class="underline copy-input">How do I create a proper order</span>**
- **<span class="underline copy-input">What are the hazards of dust</span>**
- ...

Please use me to help you go green.
`;

    ai_message_init.innerHTML = marked.parse(init_text);

    $('.copy-input').click(function () {
        user_input.value = $(this).text();
        $(this).blur();
        $(this).parents().blur();
        user_input.focus();
    });

    const m = new marked.Renderer();
    marked.use({
        renderer: m,
        gfm: true,
        breaks: false,
    });

    document.getElementById('ai-chat-open-btn').onclick = function () {
        ai_chat_container.style.opacity = '1';
        ai_chat_container.style.visibility = 'visible';
        ai_chat_container.style.height = '80dvh';
        open = true;
    };

    document.getElementById('ai-chat-close-btn').onclick = function () {
        ai_chat_container.style.opacity = '0';
        ai_chat_container.style.visibility = 'hidden';
        ai_chat_container.style.height = '0';
        ai_chat_scroll.style.visibility = 'hidden';
        open = false;
    };

    ai_chat_scroll.onclick = function () {
        ai_chat_messages.scrollTop = ai_chat_messages.scrollHeight;
        ai_chat_scroll.style.visibility = 'hidden';
    };

    document.getElementById('ai-chat-send-btn').onclick = function () {
        sendMessage();
        console.log(marked.parse('I am using __markdown__.'));
    };
    // 新增部分：回车发送消息
    user_input.addEventListener('keydown', function (event) {
        if (event.key === "Enter") {
            event.preventDefault();  // 防止表单默认提交
            sendMessage();  // 发送消息
        }
    });

    ai_chat_messages.addEventListener('scroll', function () {
        if (open) {
            checkScrollVisibility();
        }
    })

    // 定义检查滚动条可见性的函数
    function checkScrollVisibility() {
        let isBottom = ai_chat_messages.scrollHeight - ai_chat_messages.scrollTop === ai_chat_messages.clientHeight;
        ai_chat_scroll.style.visibility = isBottom ? 'hidden' : 'visible';
    }


    function sendMessage() {
        if (user_input.value.trim() !== "") {
            let userBubble = createMessageBubble('user-message');
            userBubble.textContent = user_input.value;
            getAIResponse(user_input.value);
            user_input.value = "";
        } else {
            Swal.fire({
                title: "the message can not be empty",
                icon: "info",
                closeOnClickOutside: true,
                closeOnEsc: true,
                timer: 3000,
                timerProgressBar: true,
            });
        }
    }


    function createMessageBubble(className) {
        let messageContainer = document.createElement('div');
        messageContainer.classList.add('message-container');
        let messageDiv = document.createElement('div');
        let icon = document.createElement('i');
        messageDiv.classList.add('message-bubble', className);
        messageDiv.setAttribute('tabindex', '0');  // 设置 tabindex 属性
        messageDiv.addEventListener('click', function () {
            this.focus();  // 获取焦点
        });
        messageDiv.addEventListener('keydown', function (event) {
            if ((event.ctrlKey || event.metaKey) && event.key === 'a') {
                event.preventDefault(); // 阻止默认的全选行为
                let selection = window.getSelection(); // 获取当前的选择
                let range = document.createRange(); // 创建一个范围
                range.selectNodeContents(this); // 设置范围包括此元素的内容
                selection.removeAllRanges(); // 清除当前的选择
                selection.addRange(range); // 添加新的范围
            }
        });
        if (className === 'user-message') {
            icon.classList.add('iconfont', 'icon-wode', 'iconheader');
            messageContainer.appendChild(messageDiv)
            messageContainer.appendChild(icon)
        } else {
            icon.classList.add('iconfont', 'icon-jiqiren', 'iconheader');
            messageContainer.classList.add('ai');
            messageContainer.appendChild(icon)
            messageContainer.appendChild(messageDiv)
        }
        ai_chat_messages.appendChild(messageContainer);
        ai_chat_messages.scrollTop = ai_chat_messages.scrollHeight;
        return messageDiv;
    }

    async function getAIResponse(content) {
        const response = await fetch(aiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({message: content}),
        });
        const reader = response.body.getReader();
        let aiBubble = createMessageBubble('ai-message');
        let totalText = ''; // 用于累积读取的文本
        while (true) {
            const {done, value} = await reader.read();
            totalText += decoder.decode(value);
            aiBubble.innerHTML = marked.parse(totalText);
            if (done) {
                break;
            }
        }
    }
});