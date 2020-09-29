
function showModal(modalId){
    const modal = document.getElementById(modalId);
    modal.style.display = "block";
}

function hideModal(modalId){
    const modal = document.getElementById(modalId);
    modal.style.display = "none";

    const toRemove = document.getElementsByClassName("remove-on-close");
    console.log(toRemove);
    for (const removable of toRemove){
        removable.remove();
    }
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    console.log(event.target);
    if (event.target.classList.contains("background")) {
        hideModal(event.target.id)
    }
}