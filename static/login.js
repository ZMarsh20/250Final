var user = document.getElementById("user");
var username = document.getElementById("username");
var password = document.getElementById("password");
var pass = document.getElementById("pass");
var submit = document.getElementById("submit");

var newuser = document.getElementById("newuser");
var newusername = document.getElementById("newusername");
var newpassword = document.getElementById("newpassword");
var newpass = document.getElementById("newpass");
var newpassword2 = document.getElementById("newpassword2");
var newpass2 = document.getElementById("newpass2");
var submit2 = document.getElementById("submit2");
var _name = document.getElementById("name");
var lname = document.getElementById("lname");

var sign = document.getElementById("signup");
var log = document.getElementById("login");
var signupform = document.getElementById("signupform");

user.style.display = "block";
username.style.display = "block";
password.style.display = "block";
pass.style.display = "block";
submit.style.display = "block";

log.style.display = "none";
sign.style.display = "block";

newuser.style.display = "none";
newusername.style.display = "none";
newpassword.style.display = "none";
newpass.style.display = "none";
newpassword2.style.display = "none";
newpass2.style.display = "none";
submit2.style.display = "none";
_name.style.display = "none";
lname.style.display = "none";


function signup() {
    user.style.display = "none";
    username.style.display = "none";
    password.style.display = "none";
    pass.style.display = "none";
    submit.style.display = "none";
        
    log.style.display = "block";
    sign.style.display = "none";
    
    newuser.style.display = "block";
    newusername.style.display = "block";
    newpassword.style.display = "block";
    newpass.style.display = "block";
    newpassword2.style.display = "block";
    newpass2.style.display = "block";
    submit2.style.display = "block";
    _name.style.display = "block";
    lname.style.display = "block";
}
function login() {
    user.style.display = "block";
    username.style.display = "block";
    password.style.display = "block";
    pass.style.display = "block";
    submit.style.display = "block";

    log.style.display = "none";
    sign.style.display = "block";
    
    newuser.style.display = "none";
    newusername.style.display = "none";
    newpassword.style.display = "none";
    newpass.style.display = "none";
    newpassword2.style.display = "none";
    newpass2.style.display = "none";
    submit2.style.display = "none";
    _name.style.display = "none";
    lname.style.display = "none";
}
function check() {
    if (newpassword.value === newpassword2.value) {
        if ( newusername == "" ){
            alert("Please make sure all fields are filled");
            newusername.style.backgroundColor = "red";
        } 
        else {
            if (_name.value != "") {
                if (newpassword.value == "") {
                    alert("Please make sure all fields are filled");
                } else {
                    signupform.submit();
                }
            }
            else {
                alert("Please make sure all fields are filled");
                _name.style.backgroundColor = "red";
            }
        }
    }
    else {
        alert("Your passwords do not match");
        newpassword.style.backgroundColor = "red";
        newpassword2.style.backgroundColor = "red";
    }
}
function normal() {
    newpassword.style.backgroundColor = "white";
    newpassword2.style.backgroundColor = "white";
    _name.style.backgroundColor = "white";
    newusername.style.backgroundColor = "white";
}
function usernameTaken() {
    alert("Username taken. Try again");
    newusername.style.backgroundColor = "red";
}
function tryAgain() {
    alert("Username or password incorrect");
    username.style.backgroundColor = "red";
    password.style.backgroundColor = "red";
}