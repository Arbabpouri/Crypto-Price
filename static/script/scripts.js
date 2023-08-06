const navigateToTopElement = document.getElementById('navigateToTop')
window.addEventListener("scroll", (e) => {
    let headerHeight = document.querySelector("header").scrollHeight;
    if(window.scrollY > headerHeight)
        navigateToTopElement.style.visibility = "visible";
    else
        navigateToTopElement.style.visibility = "hidden";
})

const searchButton = document.getElementById("searchButton");
searchButton.addEventListener("click",)