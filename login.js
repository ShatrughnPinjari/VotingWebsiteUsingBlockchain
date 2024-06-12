



const form = document.getElementById("form")
if(form){
    form.addEventListener("submit",(e)=>{
        e.preventDefault()
        const username = document.getElementById("username").value ;
        const password = document.getElementById("password").value;
        console.log(username)
        console.log(password)
        login(username,password)
      
    
    })

}


async function login(username,password){
    console.log("hello")
    const user ={
        "username":username,
        "password":password
    }
    useremail = username
    window.localStorage.setItem("email",username)
    const data = await fetch("http://127.0.0.1:8080/login",{
        method:"POST",
        headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(user)
    })
    const value = await data.json()
    console.log(value)
    alert(value.message)
    if(value.code==="not found"){
        window.location.href ="/register.html"
    }
    else{
        window.location.href ="/votingpage.html"
    }
   
  
  
}











