
document.querySelectorAll('.add-compare').forEach(btn=>{
 btn.addEventListener('click',()=>alert('Added to compare'));
});

// Load saved theme
if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
}

// Toggle theme
const themeToggle = document.getElementById("themeToggle");

themeToggle?.addEventListener("click", () => {

    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }

});