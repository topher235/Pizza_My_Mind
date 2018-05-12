function verifyForm() {
    var name = document.forms['form']['name'].value;
    var email_one = document.forms['form']['email_one'].value;
    var description = document.forms['form']['description'].value;

    if(name == '') {
        alert("Please enter a name");
        return false;
    } else if(email_one == '') {
        alert("Please enter an email");
        return false;
    } else if(description == '') {
        alert("Please enter a small description");
        return false;
    } else {
        return true;
    }
}
