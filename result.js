async function getWinner(){

    const data = await fetch("http://127.0.0.1:8080/count",{
        method:"GET"
    })
    const value = await data.json()
    console.log(value);

}




