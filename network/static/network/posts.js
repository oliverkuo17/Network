document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelectorAll('.like').forEach(btn => btn.addEventListener('click', () => toggle_like(btn.dataset.postId)));
  });


function toggle_like(post_id) {
    fetch(`/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            post_id: post_id
        })
    })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);
        return false

};