function loadComments() {
    const commentsContainer = document.getElementById('comments-container');
    const url = commentsContainer.getAttribute('data-url');
    
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);    
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    xhr.onload = function() {
        if(xhr.status === 200) {
            let comments = JSON.parse(xhr.responseText);
            let commentsContainer = document.getElementById('comments-container');
            commentsContainer.innerHTML = '';
            comments.forEach(comment => {
                let commentElement = document.createElement('div');
                commentElement.textContent = comment.text;
                commentsContainer.appendChild(commentElement);
            });
        }
    };

    xhr.send();
}

// Load comments when the page loads
document.addEventListener('DOMContentLoaded', function() {
    loadComments();
})
