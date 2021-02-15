
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

// This works, but I need to dynamically change them
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

// See if jquery even works
function changeDD02(value) {
    $("#dd_part").change(function() {
        if (value == 1) {
            console.log(value)
            var subpartDD = document.getElementById('dd_subpart')
            for (var i = 1; i <= 18; i++){
                var lst = document.createElement('option')
                lst.textContent = i
                lst.value = i
                subpartDD.appendChild(lst)
            }
        } else {
            console.log(value)
            document.getElementById('dd_subpart').innerHTML = '<option>dev02</option>'
        }
       //$("#second-choice").load("js/txt/" + $(this).val() + ".txt");
    });
};

$(function() {
    $('#first-choice').change(function() {
       $('#second-choice').load('../js/txt/' + $(this).val() + '.txt');
    });
});

//function devJquery() {
//};
//devJquery();

// console.log = print
function dev01() {
    console.log('ugh')
};

// Load JSON
//function jsonDev() {
//    $.getJSON('json/parts.json', function(data) {
//        console.log(data);
//    });
//}
//jsonDev();


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
