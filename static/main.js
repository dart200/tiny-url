
let tooltip;

const onCopy = (evt) => {
  evt.preventDefault();
  const urlEle = document.getElementById("url-a");
  navigator.clipboard.writeText(urlEle.innerText);
  
  tooltip.toggleEnabled();
  tooltip.show();
  setTimeout(() => tooltip.toggleEnabled(), 1000);
};

window.onload = () => {
  const urlEle = document.getElementById('url-a')
  console.log({urlEle})
  tooltip = new bootstrap.Tooltip(urlEle);
  tooltip.disable();
};

// myTooltipEl.addEventListener('hidden.bs.tooltip', function () {
//   // do something...
// });

