class Event {
    constructor(title, description) {
        this.title = title;
        this.description = description;
    }
}


let dragging = null;


// 清除指定类名
function cleanClass(className) {
    document.querySelectorAll(`.${className}`).forEach(el => {
        el.classList.remove(className);
    });
}


// 获取鼠标下方的元素
function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.draggable:not(.dragging)')];

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return {offset, element: child};
        } else {
            return closest;
        }
    }, {offset: Number.NEGATIVE_INFINITY}).element;
}

// 当双击事件时展示模态框
function showDetailModal(event) {
    // 获取模态框元素
    const detailModal = document.getElementById('detail-modal');
    const detailTitle = document.getElementById('detail-title');
    const detailDescription = document.getElementById('detail-description');

    // 设置标题和描述
    detailTitle.textContent = event.title;
    detailDescription.textContent = event.description;

    // 显示模态框
    detailModal.style.display = 'block';
}

// 拖拽开始时的处理函数
function dragStartHandler(e) {
    if (e.target.classList.contains('draggable')) {
        dragging = e.target;
        dragging.classList.add('dragging');
    }
}

// 拖拽结束时的处理函数
function dragEndHandler() {
    cleanClass('dragging');
    cleanClass('new-added');
    dragging = null; // Clear the reference
}

document.addEventListener("DOMContentLoaded", function () {
    const droppables = document.querySelectorAll('.droppable');
    const createButton = document.getElementById('create');
    // 显示创建事件的模态框
    createButton.addEventListener('click', () => {
        document.getElementById('event-modal').style.display = 'block';
    });

// 关闭模态框
    document.getElementById('close-modal').addEventListener('click', () => {
        document.getElementById('event-modal').style.display = 'none';
    });

// 初始化拖拽事件
    document.addEventListener('dragstart', e => {
        if (e.target.classList.contains('draggable')) {
            dragging = e.target;
            dragging.classList.add('dragging');
        }
    });

    document.addEventListener('dragend', () => {
        cleanClass('dragging');
        cleanClass('new-added');
        dragging = null; // Clear the reference
    });
    const todoContainer = document.querySelector('.todoContainer');
// 拖拽过程中
    droppables.forEach(droppable => {
        droppable.addEventListener('dragover', e => {
            e.preventDefault();
            if (!dragging) return;

            // 获取容器内元素的中心点位置
            const afterElement = getDragAfterElement(droppable, e.clientY);
            if (afterElement == null) {
                // 如果没有元素在鼠标下方，或者容器为空，则将元素添加到容器的末尾
                droppable.appendChild(dragging);
            } else {
                // 如果有元素在鼠标下方，则将元素添加到该元素之前
                droppable.insertBefore(dragging, afterElement);
            }
            const rect = todoContainer.getBoundingClientRect(); // 获取todoContainer的边界
            const threshold = 40; // 边缘阈值，可以根据需要调整

            let scrollX = 0; // 水平滚动速度和方向
            let scrollY = 0; // 垂直滚动速度和方向

            // 检查鼠标是否接近容器的左边缘
            if (e.clientX - rect.left < threshold) {
                scrollX = -5; // 向左滚动
            }
            // 检查鼠标是否接近容器的右边缘
            else if (rect.right - e.clientX < threshold) {
                scrollX = 5; // 向右滚动
            }

            // 检查鼠标是否接近容器的上边缘
            if (e.clientY - rect.top < threshold) {
                scrollY = -5; // 向上滚动
            }
            // 检查鼠标是否接近容器的下边缘
            else if (rect.bottom - e.clientY < threshold) {
                scrollY = 5; // 向下滚动
            }

            // 执行滚动
            todoContainer.scrollBy(scrollX, scrollY);
        });
    });

    // 绑定关闭模态框事件
    document.getElementById('close-detail-modal').addEventListener('click', () => {
        document.getElementById('detail-modal').style.display = 'none';
    });


// 在模态框中创建事件并添加到DOM
    document.getElementById('submit').addEventListener('click', () => {
        const title = document.getElementById('inputTitle').value.trim();
        const description = document.getElementById('inputDescription').value.trim();
        if (!title) {
            alert('Please enter a title.');
            return;
        }

        // 创建event对象
        const newEvent = new Event(title, description);

        // 创建draggable div的内容部分
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('content');
        contentDiv.textContent = newEvent.title;

        // 创建包含删除按钮的容器
        const buttonContainer = document.createElement('div');
        buttonContainer.classList.add('button-container');

        // 创建删除按钮
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.classList.add('delete-button');
        deleteButton.onclick = function () {
            draggableDiv.remove(); // 删除这个draggable div
        };
        buttonContainer.appendChild(deleteButton);

        // 创建draggable div
        const draggableDiv = document.createElement('div');
        draggableDiv.classList.add('draggable');
        draggableDiv.draggable = true;
        draggableDiv.appendChild(contentDiv);
        draggableDiv.appendChild(buttonContainer);
        draggableDiv.ondblclick = () => showDetailModal(newEvent);

        // 添加到todo区域
        const todoDroppable = document.getElementById('todo');
        todoDroppable.appendChild(draggableDiv);

        // 清空输入并关闭模态框
        document.getElementById('inputTitle').value = '';
        document.getElementById('inputDescription').value = '';
        document.getElementById('event-modal').style.display = 'none';

        const draggables = document.querySelectorAll('.draggable');
        draggables.forEach(draggable => {
            draggable.addEventListener('dragstart', dragStartHandler);
            draggable.addEventListener('dragend', dragEndHandler);
        });

        // 添加拖拽事件监听器
        draggableDiv.addEventListener('dragstart', dragStartHandler);
        draggableDiv.addEventListener('dragend', dragEndHandler);
    });

});



