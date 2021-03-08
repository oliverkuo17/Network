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
            let ori_like = document.querySelector(`#likes${post_id}`);
            if (parseInt(result.likes_num) > parseInt(ori_like.innerHTML)) {
                document.querySelector(`[data-postid='${post_id}']`).style.color = "dodgerblue";
                document.querySelector(`[data-postid='${post_id}']`).innerHTML = "<i class='fas fa-thumbs-up'></i> Liked";
            } else {
                document.querySelector(`[data-postid='${post_id}']`).style.color = "black";
                document.querySelector(`[data-postid='${post_id}']`).innerHTML = "<i class='far fa-thumbs-up'></i> Like";
            }
            document.querySelector(`#likes${post_id}`).innerHTML = `${result.likes_num}`;
            return false;
        })


}