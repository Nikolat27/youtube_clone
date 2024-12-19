const links = document.querySelectorAll(".subscriptions-div");
const showMoreButton = document.getElementById("show-more-btn");
let currentVisibleCount = 3;

// Initially hide all but the first 3 subscriptions
links.forEach((link, index) => {
    if (index >= currentVisibleCount) {
        link.classList.add("hidden");
    }
});

showMoreButton.addEventListener("click", () => {
    links.forEach(link => {
        if (link.classList.contains("hidden")) {
            link.classList.remove("hidden");
        }
    });

    // Toggle the button text
    if (showMoreButton.textContent === "Show more") {
        console.log("hi")
        showMoreButton.textContent = "Show Less";
    } else {
        console.log("bye")
        // When user clicks on show less buttom (it only shows 3 subscription)
        for (let i = 3; i < links.length; i++) {
            links[i].classList.add("hidden");
        }
        showMoreButton.textContent = "Show more";
    }
});