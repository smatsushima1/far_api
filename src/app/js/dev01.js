
function changeName() {
    let dev_str = document.getElementById('demo')
    dev_str.innerHTML = 'Hello JavaScript!'
    };

function popPart() {
    var partDD = document.getElementById('dd_part')
    for (var i = 1; i <= 53; i++) {
        var lst = document.createElement('option')
        lst.innerHTML = i
        lst.value = i
        partDD.appendChild(lst)
        }
    };
popPart();


function popSubpart() {





    };
