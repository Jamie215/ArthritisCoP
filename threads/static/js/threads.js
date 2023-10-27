const isModeratorElement = document.getElementById('isModerator');
const isModerator = isModeratorElement.getAttribute('data-is-moderator') === 'True';

function loadSortedThreads(sortOrder, context=null, query=null) {
    let xhr = new XMLHttpRequest();
    let url = "/get_sorted_threads/?sort=" + sortOrder;

    if (context) {
        url += "&context=" + context;
    }
    if (query) {
        url += "&query=" + query;
    }

    xhr.open('GET', url, true);
    xhr.onload = function() {
        if(xhr.status === 200) {
            let threads = JSON.parse(xhr.responseText);
            let threadsContainer = document.getElementById('threads-container');
            
            // Clear the current thread table
            threadsContainer.innerHTML = '';

            threads.forEach(thread => {
                let row = document.createElement('tr');
                row.setAttribute('id', `thread-${thread.id}`);

                // Title Column
                const titleCol = document.createElement('td');
                const titleLink = document.createElement('a');
                titleLink.href = `/${thread.id}`;
                titleLink.textContent = thread.title;
                titleCol.appendChild(titleLink);

                // Description Column
                const desCol = document.createElement('td');
                desCol.textcontent = thread.description;

                // Date Column
                const dateCol = document.createElement('td');
                dateCol.textContent = thread.date;

                // Comment Count Column
                const commentCountCol = document.createElement('td');
                commentCountCol.textContent = thread.comment_count;

                // View Count Column
                const viewCountCol = document.createElement('td');
                viewCountCol.textContent = thread.view_count;

                // Additional Column for Moderators
                if (isModerator) {
                    const actionCol = document.createElement('td');
                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete'
                    deleteButton.addEventListener('click', function() {
                        deleteThread(thread.id);
                    });
                    actionCol.appendChild(deleteButton);
                    row.append(actionCol);
                }

                row.append(titleCol);
                row.append(desCol);
                row.append(dateCol);
                row.append(commentCountCol);
                row.append(viewCountCol);

                threadsContainer.appendChild(row);
            });
        }
    };
    xhr.send();
}

function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}

function deleteThread(threadId) {
    let xhr = new XMLHttpRequest();
    xhr.open('DELETE', `/delete_thread/${threadId}/`, true);

    // Set the CSRF token
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));

    xhr.onload = function() {
        if (xhr.status === 200) {
            const threadRow = document.getElementById(`thread-${threadId}`);
            if (threadRow) {
                threadRow.remove();
            }
        }
        else {
            console.error('Failed to delete thread: ', xhr.responseText);
        }
    };
    xhr.send();
}

// Load threads initially
document.addEventListener('DOMContentLoaded', function() {
    let sortOrder = 'recent'; // Default sorting
    let context = document.body.getAttribute('data-context');
    let query = document.body.getAttribute('data-query');
    
    loadSortedThreads(sortOrder, context, query);
});

// Attach the function to buttons or other UI elements
document.getElementById('sort-most-recent').addEventListener('click', function() {
    loadSortedThreads('recent');
});

document.getElementById('sort-most-views').addEventListener('click', function() {
    loadSortedThreads('views');
});
