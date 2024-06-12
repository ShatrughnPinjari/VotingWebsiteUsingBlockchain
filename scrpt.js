


function generateString(length) {
    const characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = ' ';
    const charactersLength = characters.length;
    for ( let i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }

    return result;
}


function vote(){

    console.log("triggered")
    document.getElementById("c").style.display="block"
}

function set(){
    console.log("triggered")
    document.getElementById("c").style.display="none"
}


async function fetching(){


    const data = await fetch("http://127.0.0.1:8080/counts",{
        method:"GET"
    })
    const value = await data.json()
    console.log(value);
    const win = document.getElementById("win")
    if(win){
   
        win.innerHTML=`<h3 style="color:orange;font-weight:bold">${value.winner}</h3> keeping all candiates behind by <h3 style="color:red">${value.votes}</h3> votes`;
   
   
    }
}

fetching()




async function giveVote(candidate){

    const useremail = window.localStorage.getItem("email")
    const id = generateString(5);

    let user ={
        voters_id:useremail,
        vote:`${candidate}`
    }

try {
    const data = await fetch("http://127.0.0.1:8080/new-vote",{
        method:"POST",
        headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(user)
    })

const result = await data.json()
console.log(result)
alert(result.message)
    document.getElementById("button").style.backgroundColor="rgba(217,217,217,1)";

} catch (error) {
    console.log(error)
    alert("sever error")
}
}