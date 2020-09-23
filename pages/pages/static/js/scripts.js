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