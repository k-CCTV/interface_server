function searchFunc() {
  let search = document.querySelector(".search-bar").value.toLowerCase();
  let listInner = document.getElementsByClassName("cctv-row");

  for (let i = 0; i < listInner.length; i++) {
    title = listInner[i].getElementsByClassName("searchTitle");
    author = listInner[i].getElementsByClassName("searchAuthor");
    content = listInner[i].getElementsByClassName("searchContent");
    if (
      title[0].innerHTML.toLowerCase().indexOf(search) != -1 ||
      author[0].innerHTML.toLowerCase().indexOf(search) != -1 ||
      content[0].innerHTML.toLowerCase().indexOf(search) != -1
    ) {
      listInner[i].style.display = "flex";
    } else {
      listInner[i].style.display = "none";
    }
  }
}

document.querySelector(".jsFilter").addEventListener("click", function () {
  document.querySelector(".filter-menu").classList.toggle("active");
});

document.querySelector(".grid").addEventListener("click", function () {
  document.querySelector(".list").classList.remove("active");
  document.querySelector(".grid").classList.add("active");
  document.querySelector(".cctv-area-wrapper").classList.add("gridView");
  document.querySelector(".cctv-area-wrapper").classList.remove("tableView");
});

document.querySelector(".list").addEventListener("click", function () {
  document.querySelector(".list").classList.add("active");
  document.querySelector(".grid").classList.remove("active");
  document.querySelector(".cctv-area-wrapper").classList.remove("gridView");
  document.querySelector(".cctv-area-wrapper").classList.add("tableView");
});

var modeSwitch = document.querySelector(".mode-switch");
modeSwitch.addEventListener("click", function () {
  document.documentElement.classList.toggle("light");
  modeSwitch.classList.toggle("active");
});
