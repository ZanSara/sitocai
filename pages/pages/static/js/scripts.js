/***************************/
/*          MENU            
/***************************/
function toggleMenu(){
    var nav = document.getElementById("sidenav");
    var menu = document.getElementById("menu");
    var footer = document.getElementById("footer");
  
    if (!menu.style.display || menu.style.display === "none"){
        // Expand
        nav.style.height = "100vh";
        nav.style.textAlign = "center";
        menu.style.display = "block";
        menu.style.width = "100%";
        menu.style.margin = "0";
        menu.style.padding = "0";
        footer.style.display = "block";
        document.body.style.overflowY = "hidden";
    } else {
        // Collapse
        nav.style.height = "var(--navbar-height)";
        menu.style.display = "none";
        footer.style.display = "none";
        document.body.style.overflowY = "auto";
    }
}


/***************************/
/*       CAROUSEL            
/***************************/
function moveRight(carouselId){
    const carousel = document.getElementById(carouselId)
    const slides = carousel.querySelectorAll('.slide');
    
    var slideId = +carousel.dataset.activeSlide+1;
    if (slideId >= slides.length){
        slideId = 0;
    }
    carousel.dataset.activeSlide = slideId;

    for (slide of slides){
        slide.classList.remove('active');
    }
    slides[slideId].classList.add('active');
}

function moveLeft(carouselId){
    const carousel = document.getElementById(carouselId)
    const slides = carousel.querySelectorAll('.slide');
    
    var slideId = +carousel.dataset.activeSlide-1;
    if (slideId < 0){
        slideId = slides.length-1;
    }
    carousel.dataset.activeSlide = slideId;

    for (slide of slides){
        slide.classList.remove('active');
    }
    slides[slideId].classList.add('active');
}

/***************************/
/*        MODAL            
/***************************/
function showModal(modalId, callback){
  if (callback){ callback(); }
  const modal = document.getElementById(modalId);
  modal.style.opacity = 1;
  modal.style.pointerEvents = "auto";
}

function hideModal(modalId){
  const modal = document.getElementById(modalId);
  modal.style.opacity = 0;
  modal.style.pointerEvents = "none";

  // Reset LOGIN form
  setTimeout(() => {
    const toRemove = document.getElementsByClassName("remove-on-close");
    for (const removable of toRemove){
        removable.remove();
    }

    // Reset NUOVA form
    resetNuovaForm();

    // Reset CERCA form
    const forms = document.getElementsByClassName("modal-form");
    for (const elem of forms){
        elem.style.display = 'block';
    }
    const loading = document.getElementsByClassName("loading");
    for (const elem of loading){
        elem.style.display = 'none';
    }
    const results = document.getElementsByClassName("results");
    for (const elem of results){
        elem.style.display = 'none';
    }
  }, 500)
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target.classList.contains("background")) {
      hideModal(event.target.id)
  }
}



/***************************/
/*        AJAX            
/***************************/
function submitModal(modalId, url, callback){
    const form = document.getElementById(modalId).getElementsByTagName('form')[0];
    form.style.display = "none";
    const loading = document.getElementById(modalId).getElementsByClassName('loading')[0];
    loading.style.display = "block";

    fetch(url, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(data => {
        callback(data);
        loading.style.display = 'none';
        const results = document.getElementById(modalId).getElementsByClassName('results')[0];
        results.style.display = "block";
    });
}


/***************************/
/*      PRENOTAZIONI            
/***************************/
function toggleGestione(){
    const titolo = document.getElementById('Nuova_Modal').getElementsByClassName('title')[0].getElementsByTagName('h2')[0];
    const posti = document.getElementById('nuova-posti');
    const postiLabel = document.getElementById('nuova-posti-label');
    
    if (document.getElementById('nuova-gestione').checked){
        titolo.innerText = "Nuova Gestione";
        posti.disabled = true;
        posti.style.display = 'none';
        postiLabel.style.display = 'none';
    } else {
        titolo.innerText = "Nuova Prenotazione";
        posti.disabled = false;
        posti.style.display = 'block';
        postiLabel.style.display = 'block';
    }
}

function resetNuovaForm(){
    const modal = document.getElementById('Nuova_Modal');
    const form = modal.getElementsByTagName('form')[0];
    form.reset();

    const titolo = modal.getElementsByClassName('title')[0].getElementsByTagName('h2')[0];
    titolo.innerText = "Nuova Prenotazione";

    const posti = document.getElementById('nuova-posti');
    const postiLabel = document.getElementById('nuova-posti-label');
    posti.disabled = false;
    posti.style.display = 'block';
    postiLabel.style.display = 'block';
}
  
// Ottiene la disponibilita' di letti per la data selezionata e per la durata selezionata
document.querySelector('#nuova-arrivo').addEventListener('input', function (e) {
    getAvailabilityForDates();
});
document.querySelector('#nuova-durata').addEventListener('input', function (e) {
    getAvailabilityForDates();
});

function getAvailabilityForDates(){
    arrivo = document.getElementById("nuova-arrivo").value;
    durata = document.getElementById("nuova-durata").value;
    fetch('/rifugio/prenotazioni/disponibilita?' + new URLSearchParams({
        arrivo: new Date(arrivo).getTime(),
        durata: +durata,
    }))
    .then(response => response.json())
    .then(data => {
        if(data['errors'].length === 0){        
            document.getElementById('nuova-disponibilita').innerText = data['letti']+" letti + "+data['emergenza']+" brandine";
        } else {
            document.getElementById('nuova-disponibilita').innerText = "seleziona data e n. notti valide";
        }
    });
}




function prepareNuovaValidation(){

}
