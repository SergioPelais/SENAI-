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


const bntNotf = document.getElementById('btn-notf')
const boxNotf = document.getElementsByClassName('notification')[0]
const closeNotf = document.getElementById('fechar-notf')
function abrirNotf(){
  bntNotf.classList.add('abrir-notf')
  boxNotf.classList.add('abrir-notf-box')
  boxNotf.classList.remove('fechar-notf-box')

}
function fecharNotf(){
  boxNotf.classList.add('fechar-notf-box')
  bntNotf.classList.remove('abrir-notf')
  boxNotf.classList.remove('abrir-notf-box')

}