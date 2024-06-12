

const form = document.getElementById("form")
if(form){
    form.addEventListener("submit",(e)=>{
        e.preventDefault()
        const username = document.getElementById("username").value ;
        const password = document.getElementById("password").value;
        const number = document.getElementById("number").value;
        register(username,password,number)
        
    
    })

}


async function register(username,password,number){
    console.log("hello")
    const user ={
        "username":username,
        "password":password,
        "number":number
    }
    useremail = username
    const data = await fetch("http://127.0.0.1:8080/register",{
        method:"POST",
        headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(user)
    })
  
    const value = await data.json()
    console.log(value); 
    alert(value)
    window.location.href ="/login.html"
}


