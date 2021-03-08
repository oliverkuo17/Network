document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle like
    document.querySelectorAll('.like').forEach(btn => btn.addEventListener('click', () => toggle_like(btn.dataset.postid)));
  });


function toggle_like(post_id) {
    fetch(`/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            toggle_like: true
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            document.querySelector(`#likes${post_id}`).innerHTML = `likes: ${result.likes_num}`;
        })


}