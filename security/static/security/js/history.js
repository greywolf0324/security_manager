

$(document).ready(function() {
    function toggleCheckboxes(masterCheckbox) {
    var checkboxes = document.getElementsByClassName("subCheckbox");
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = masterCheckbox.checked;
    }
    }

    function updateMasterCheckbox() {
    var masterCheckbox = document.getElementById("masterCheckbox");
    var checkboxes = document.getElementsByClassName("subCheckbox");
    masterCheckbox.checked = true;
    for (var i = 0; i < checkboxes.length; i++) {
        if (!checkboxes[i].checked) {
        masterCheckbox.checked = false;
        break;
        }
    }
    }

    $("#checkbox-all").onchange(
        toggleCheckboxes("#checkbox-all")
    )
})