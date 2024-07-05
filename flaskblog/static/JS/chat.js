var messages = "";

function setup() {
    chat_window = document.getElementById("chat_window");
    let user = document.getElementById('author').value;
    getMessages(user)
    console.log(user);
    document.getElementById("new_message_submit").addEventListener("click", newMessage);
}

function newMessage() {
    let message = document.getElementById('message').value;
    let room = document.getElementById('currentroom').innerText;
    let author = document.getElementById('author').value;
    if (message === '') {
        return false;
    }
    fetch("/new_message/", {
        method: "POST",
        headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
        body: `message=${message}&author=${author}&room=${room}`
    })
        .then((response) => response.json())
        .then((results) => {
            let current_set = results[0];
            let temp = `<p class="fw-bold"> ${current_set['author']}: ${current_set['message']}:${current_set['room']}</p><hr>`;
            chat_window.innerHTML += temp;
        })
        .catch((e) => {
            console.log('Error getting the new message: ', e)
        })
}

 
function getMessages(author) {
    fetch("/messages/", 
    )
    .then((response) => response.json())
    .then((results) => {
            let chat_window = document.querySelector("#data-output"); 
            var tempMessages = "";
            for (index in results) {
                let current_set = results[index];
                if (current_set['author']==author)
                {
                    tempMessages += `
                    <tr>
                    <td class="text-muted">${current_set['author']} 
                       <div class="card" >
                       <p  float="right">${current_set['message']}</p>
                       </div>
                       </td>
                       
                    </tr>
                 `;
                }
                else{
                    tempMessages += `
                    <tr>
                    <td class="text-muted">${current_set['author']} 
                       <div class="card" >
                       <p style:"background-color:white">${current_set['message']}</small>
                       </div>
                       </td>
                       
                    </tr>
                 `;

                }

                //`<p class="fw-bold"> ${current_set['author']}:${current_set['message']}</p><hr>`;
            }
            if (tempMessages !== messages) {
                messages = tempMessages;
                chat_window.innerHTML = messages;
            }
            else{
                messages = `<p>error</p>`
            }
        })
    setTimeout(getMessages, 200);
};

window.addEventListener('load', setup);
