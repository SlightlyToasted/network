document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#all-posts-btn').addEventListener('click', () => load_view("all"));
    document.querySelector('#new-post-btn').addEventListener('click', () => load_view("new"));

    //Button to create a new post
    document.querySelector('#create').addEventListener('click', create_post);
  
    // By default, load all posts
    load_view("all");
   
  });


function load_view(view) {
    if (view == "all"){
        document.querySelector('#all-posts').style.display = 'block';
        document.querySelector('#new-post').style.display = 'none';
        // get posts

        fetch('/posts/posts')
        .then(response => response.json())
        .then(posts => {
            //create post for each email
            posts.forEach(posts => {
                //create elements
                const post_container = document.createElement('div');
                const username = document.createElement('p');
                const content = document.createElement('p');
                const timestamp = document.createElement('p');
                const likes = document.createElement('p');

                username.innerHTML = posts.user;
                content.innerHTML = posts.content;
                timestamp.innerHTML = posts.timestamp;
                likes.innerHTML = "0 likes";

                post_container.setAttribute("id", "post-container");

                document.querySelector('#all-posts').append(post_container);
                post_container.append(username);
                post_container.append(content);
                post_container.append(timestamp);
                post_container.append(likes);
            })
        })





    }
    if (view == "new") {
        document.querySelector('#all-posts').style.display = 'none';
        document.querySelector('#new-post').style.display = 'block';
        }
}

function create_post(){
    console.log("Loaded all posts");
    let content = document.querySelector('#post-body').value;
    fetch('/posts', {
    method: 'POST',
        body: JSON.stringify({
            content: content
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        load_view("all");
    });
}