
function changeName() {
    let dev_str = document.getElementById('demo')
    dev_str.innerHTML = 'Hello JavaScript!'
    };

// Populate part first
function popPart() {
    var partDD = document.getElementById('dd_part')
    for (var i = 1; i <= 53; i++) {
        var lst = document.createElement('option')
        lst.textContent = i
        lst.value = i
        partDD.appendChild(lst)
        }
    };
popPart();

// Can't get jquery to work
function changeDD(value) {
    if (value == 1) {
        var subpartDD = document.getElementById('dd_subpart')
        for (var i = 1; i <= 16; i++){
            var lst = document.createElement('option')
            lst.textContent = i
            lst.value = i
            subpartDD.appendChild(lst)
        }
    } else {
        document.getElementById('dd_subpart').innerHTML = '<option>Nope</option>'
    }
};




// Subparts are determined by what part is chosen
//function popSubpart() {
//    $('#dd_part').change(function() {
//    var $dropdown = $(this)
//    $.getJSON('json/parts.json', function(data) {
//        var key = $dropdown.val()
//        var vals = 0
//        switch(key) {
//            case 1:
//                vals = 5
//                break
//            case 2:
//                vals = 10
//                break
//            case 3:
//                vals = 15
//                break
//            };
//
//        var $dd_subpart = $('#dd_subpart')
//        $dd_subpart.empty()
//        for (var i = 1; i <= vals; i++) {
//            var lst = document.createElement('option')
//            lst.textContent = i
//            lst.value = i
//            $dd_subpart.appendChild(lst)
//            };
//        };
//    });
//};
