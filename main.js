document.getElementById("add_student").onclick = duplicate;

var i = 0;
var original = document.getElementById("student_groups");

function duplicate() {
    var clone = original.cloneNode(true);
    clone.id = "student_groups" + ++i;
    original.parentNode.appendChild(clone);
}
