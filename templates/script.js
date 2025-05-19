// alert("loading");

function addNewWEField(){
	// console.log("Adding new Field")
let newNode=document.createElement("textarea");
newNode.classList.add("form-control");
newNode.classList.add("weField");
newNode.classList.add("mt-2");
newNode.setAttribute("rows",3);
newNode.setAttribute('placeholder','Enter here');

let weOb=document.getElementById("we");
let weAddButtonOb=document.getElementById("weAddButton");

weOb.insertBefore(newNode,weAddButtonOb); 

}

function addNewAQField(){
	// console.log("Adding new Field")
let newNode=document.createElement("textarea");
newNode.classList.add("form-control");
newNode.classList.add("eqField");
newNode.classList.add("mt-2");
newNode.setAttribute("rows",3);
newNode.setAttribute('placeholder','Enter here');

let aqOb=document.getElementById("aq");
let aqAddButtonOb=document.getElementById("aqAddButton");

aqOb.insertBefore(newNode,aqAddButtonOb); 

}


function generateCV(){

// console.log("Generating CV")

let nameField=document.getElementById("nameField").value;
let nameT1=document.getElementById("nameT1");
nameT1.innerHTML=nameField;

document.getElementById("nameT2").innerHTML=document.getElementById("nameField").value;


let contactField=document.getElementById("contactField").value;
let contactT1=document.getElementById("contactT");
contactT1.innerHTML=contactField;


let addressField=document.getElementById("addressField").value;
let addressT1=document.getElementById("addressT");
addressT1.innerHTML=addressField;

let file = document.getElementById("imgField").files[0];
let reader = new FileReader();

reader.onloadend = function () {
    document.getElementById("imgTemplate").src = reader.result;
};

if (file) {
    reader.readAsDataURL(file);
}

document.getElementById("fbT").innerHTML=document.getElementById("fbField").value;
document.getElementById("instaT").innerHTML=document.getElementById("instaField").value;
document.getElementById("linkedT").innerHTML=document.getElementById("linkedField").value;

//objective
document.getElementById("objectiveT").innerHTML=document.getElementById("objectiveField").value;

//we

let wes=document.getElementsByClassName('weField');
let str=" ";

for(let e of wes)
{
	str=str+`<li> ${e.value} </li>`;
}

document.getElementById("weT").innerHTML=str;

//aq

let aqs=document.getElementsByClassName('eqField');
let str1=" ";

for(let e of aqs)
{
	str1+=`<li> ${e.value} </li>`;
}

document.getElementById("aqT").innerHTML=str1;

document.getElementById("cv-form").style.display="none";
document.getElementById("cv-template").style.display="block";

}

function printCV()
{
	window.print();
}
function downloadCV() {
    const element = document.getElementById("cv-template");
    const opt = {
        margin:       0,
        filename:     'my_resume.pdf',
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2 },
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
    };

    html2pdf().set(opt).from(element).save();
}