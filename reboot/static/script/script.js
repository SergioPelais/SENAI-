function load(cod) {
  if (cod.value.trim()) {
    document.getElementsByClassName('load')[0].style.display = 'flex'
  }
}

const btnTopo = document.getElementById("btnTopo");

let ativo = false
// Mostrar o botão ao descer 200px
window.addEventListener("scroll", () => {
  if (window.scrollY > 150) {
    btnTopo.classList.remove('fecharTopo')
    btnTopo.classList.add('abrirTopo')
    ativo = true
  } else if (ativo) {
    btnTopo.classList.add('fecharTopo')
    btnTopo.classList.remove('abrirTopo')
  } 
});

// Rolar suavemente até o topo
btnTopo.addEventListener("click", () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
});
