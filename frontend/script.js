let userProfile = {
    age:30,
    income:null,
    investment:null,
    risk:"Medium"
}

/* CLOSE */
function closeChat(){
    document.getElementById("chatbot").style.display="none"
}

/* OPEN */
function openChat(){
    document.getElementById("chatbot").style.display="block"
}

/* SEND */
async function sendMessage(){

let input=document.getElementById("chat-input")
let message=input.value.trim()

if(message==="") return

appendMessage("You",message)
input.value=""

let reply=await processMessage(message)

appendMessage("Advisor",reply)

}

/* APPEND */
function appendMessage(sender,text){

let chat=document.getElementById("chat-body")

chat.innerHTML+=`<p><b>${sender}:</b> ${text}</p>`
chat.scrollTop=chat.scrollHeight

}

/* PROCESS */
async function processMessage(message){

let msg=message.toLowerCase()
let value=null

let nums=message.match(/\d+/g)

if(nums){
value=parseInt(nums[0])
if(msg.includes("lakh")) value*=100000
}

/* GREETING */
if(msg.includes("hi")){
return "Hey 👋 Tell me your income and investment amount."
}

/* INCOME */
if(msg.includes("income")){
userProfile.income=value
return "Nice 👍 How much do you want to invest?"
}

/* INVEST */
if(msg.includes("invest")){
userProfile.investment=value
return await generatePlan()
}

/* UPDATE */
if(msg.includes("change") && value){
userProfile.income=value
return await generatePlan()
}

return "Tell me your income and investment."
}

/* GENERATE */
async function generatePlan(){

let res=await fetch("/recommend",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify(userProfile)
})

let data=await res.json()

displayPortfolio(data)

return "Done 👍 Portfolio updated."
}

/* BUTTON */
async function getRecommendation(){

userProfile.age=parseInt(document.getElementById("age").value)
userProfile.income=parseInt(document.getElementById("income").value)
userProfile.investment=parseInt(document.getElementById("amount").value)
userProfile.risk=document.getElementById("risk").value

let res=await fetch("/recommend",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify(userProfile)
})

let data=await res.json()

displayPortfolio(data)

}

/* DISPLAY */
function displayPortfolio(data){

let html="<h3>Recommended Portfolio</h3>"

for(let s in data.portfolio){
html+=`<p><b>${s}</b> — ₹${data.portfolio[s]}</p>`
}

html+=`<p>${data.strategy}</p>`

document.getElementById("result").innerHTML=html

let market=""

data.market.forEach(s=>{
market+=`<div class="market-card">${s.name}<br>₹${s.price}</div>`
})

document.getElementById("market").innerHTML=market

}

/* ENTER */
document.addEventListener("DOMContentLoaded",()=>{
document.getElementById("chat-input").addEventListener("keypress",(e)=>{
if(e.key==="Enter") sendMessage()
})
})