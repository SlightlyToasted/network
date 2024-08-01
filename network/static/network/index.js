document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#all-posts-btn').addEventListener('click', () => load_view("all"));
    document.querySelector('#new-post-btn').addEventListener('click', () => load_view("new"));

    //Button to create a new post
    document.querySelector('#create').addEventListener('click', create_post);
  
    // By default, load all posts
    load_view("new");
   
  });


function load_view(view) {
    if (view == "all"){
        document.querySelector('#all-posts').style.display = 'block';
        document.querySelector('#new-post').style.display = 'none';
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