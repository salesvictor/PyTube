// main js script file
function expand() {
  var header = document.getElementById("navbarHeader")
  var div = document.getElementById("expand")
  if (header.classList.contains('show')) {
    div.style.paddingTop = '0'
  } else {
    div.style.paddingTop = '13rem'
  }
}
