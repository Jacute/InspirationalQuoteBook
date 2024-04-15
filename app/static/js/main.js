// function toggleUserMenu() {
//     const userMenu = document.getElementById('dropdown-menu');
//     userMenu.style.display = (userMenu.style.display === 'none' || userMenu.style.display === '') ? 'block' : 'none';
// }

const menuButton = document.querySelector(".users");
const menuContainer = document.querySelector(".dropdown-menu");

menuButton.addEventListener("click", () => {
  if (menuContainer.classList.contains("hidden")) {
    menuButton.classList.add("active");
    menuContainer.classList.remove("hidden");
    menuContainer.classList.add("show");
  } else {
    menuButton.classList.remove("active");
    menuContainer.classList.remove("show");
    menuContainer.classList.add("hidden");
  }
});

document.addEventListener("click", (e) => {
  if (!e.target.closest(".users") && !e.target.closest(".dropdown-menu")) {
    menuButton.classList.remove("active");
    menuContainer.classList.remove("show");
    menuContainer.classList.add("hidden");
  }
});



function toggleScrollToTopButton() {
    var scrollToTopBtn = document.getElementById('scrollToTopBtn');
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        scrollToTopBtn.style.display = 'block';
    } else {
        scrollToTopBtn.style.display = 'none';
    }
}

function scrollToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

window.onscroll = function() { toggleScrollToTopButton() };