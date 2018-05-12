var date_num = 0;
// Dynamically create a text input element
function addInput() {
    var days = document.getElementById('extra-days-js');
    var hidden_input = document.getElementById('num-extra-days-js');
    var input = document.createElement('input');
    var row = document.createElement('div');

    row.setAttribute('class', 'form-row');
    input.setAttribute('type', 'text');
    input.setAttribute('class', 'form-control date-input');
    input.setAttribute('placeholder', 'Enter a date');
    input.setAttribute('name', 'date_'+date_num);
    hidden_input.setAttribute('value', date_num+1);
    date_num++;

    row.appendChild(input);
    days.appendChild(row)
}

// Dynamically remove a text input element
function subInput() {
    var days = document.getElementById('extra-days-js');
    days.removeChild(days.lastChild);
}

$('document').ready(function() {
    var days = document.getElementById('extra-days-js');
    var hidden_input = document.createElement('input');
    hidden_input.setAttribute('id', 'num-extra-days-js');
    hidden_input.setAttribute('type', 'hidden');
    hidden_input.setAttribute('name', 'num_extra_days');
    hidden_input.setAttribute('value', date_num);
    days.appendChild(hidden_input);

    for(i = 0; i < 10; i++) {
        addInput();
    }
});
