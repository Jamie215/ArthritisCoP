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
            
                const titleCol = document.createElement('td');
                const titleLink = document.createElement('a');
                titleLink.href = '/${thread.id}';
                titleLink.textContent = thread.title;
                titleCol.appendChild(titleLink);

                const desCol = document.createElement('td');
                desCol.textcontent = thread.description;

                const dateCol = document.createElement('td');
                dateCol.textContent = thread.date;

                const commentCountCol = document.createElement('td');
                commentCountCol.textContent = thread.comment_count;

                const viewCountCol = document.createElement('td');
                viewCountCol.textContent = thread.view_count;

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

// Load threads initially
document.addEventListener('DOMContentLoaded', function() {
    let sortOrder = 'recent'; // Default sorting
    let context = document.body.getAttribute('data-context');
    let query = document.body.getAttribute('data-query');
    
    loadSortedThreads(sortOrder, context, query);
});

// Attach the function to buttons or other UI elements
document.getElementById('sort-most-recent').addEventListener('click', function() {
    loadSortedThreads('most_recent');
});

document.getElementById('sort-most-views').addEventListener('click', function() {
    loadSortedThreads('most_views');
});