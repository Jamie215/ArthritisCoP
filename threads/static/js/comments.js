const isModeratorElement = document.getElementById('isModerator');
const isModerator = isModeratorElement.getAttribute('data-is-moderator') === 'True';

function loadComments() {
    const commentsContainer = document.getElementById('comments-container');
    const url = commentsContainer.getAttribute('data-url');
    
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);    
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    xhr.onload = function() {
        if(xhr.status === 200) {
            let comments = JSON.parse(xhr.responseText);
            commentsContainer.innerHTML = '';

            if (comments.length === 0) {
                let noCommentPara = document.createElement('p');
                noCommentPara.textContent = 'No comments yet. Be the first to comment!';
                commentsContainer.appendChild(noCommentPara);
            }
            else {
                comments.forEach(comment => {
                    let commentCard = document.createElement('div');
                    commentCard.className = 'card mb-2';
                    commentCard.setAttribute('id', `comment-${comment.id}`);

                    let cardBody = document.createElement('div');
                    cardBody.className = 'card-body'
                    let commentText = document.createElement('p');
                    commentText.className = 'card-text';
                    commentText.textContent = comment.text;

                    let commentDate = document.createElement('p');
                    let smallDate = document.createElement('small');
                    smallDate.textContent = `Posted on ${comment.date}`;
                    commentDate.appendChild(smallDate);

                    let commentUpvotes = document.createElement('p');
                    commentUpvotes.textContent = `Upvotes: ${comment.upvotes}`;
                    
                    if (isModerator) {
                        const deleteButton = document.createElement('button');
                        deleteButton.addEventListener('click', function() {
                            deleteComment(comment.id);
                        })
                        commentCard.appendChild(deleteButton);
                    }

                    cardBody.appendChild(commentText);
                    cardBody.appendChild(commentDate);
                    cardBody.appendChild(commentUpvotes);

                    commentCard.appendChild(cardBody);
                    commentsContainer.appendChild(commentCard);
                });
            }
        }
    };
    xhr.send();
}

function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}

function deleteComment(commentId) {
    let xhr = new XMLHttpRequest();
    xhr.open('DELETE', `/delete_comment/${commentId}/`, true);

    // Set the CSRF token
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));

    xhr.onload = function() {
        if (xhr.status === 200) {
            const commentRow = document.getElementById(`comment-${commentId}`); 
            if (commentRow) {
                commentRow.remove();
            }
        }
        else {
            console.error('Failed to delete comment: ', xhr.responseText);
        }
    };
    xhr.send();
}

// Load comments when the page loads
document.addEventListener('DOMContentLoaded', function() {
    loadComments();
})