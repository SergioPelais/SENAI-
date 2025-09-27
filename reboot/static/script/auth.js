const at = document.getElementById('atividade')
at.value = 'Saída'
function opcao(num = 0) {
    at.value = num
}
const boxCaso = document.querySelectorAll('.boxCaso');
boxCaso.forEach(n =>
    n.addEventListener('click', function () {
        const caso = document.getElementById("caso")
        caso.style.transform = "translateX(100%)"
    })
)

const tagBox = document.getElementsByClassName('tags')[0]
const tags = ['Trabalho', 'Médico', 'Dentista', 'Outros']

tags.forEach(e => tagBox.innerHTML += `
    <button class="itemTag" type="button" value="${e}">${e}</button>
    `)

const itemTag = document.querySelectorAll('.itemTag')

itemTag.forEach(e => e.addEventListener('click', () => {
    itemTag.forEach(e => { e.style.backgroundColor = '#d7d7e0'; e.style.color = '#000' })
    e.style.backgroundColor = '#a1a1e0ff'
    e.style.color = '#fff'

    if (e.value === 'Outros') {
        document.getElementsByClassName('inp')[4].style.display = 'block'
        document.getElementsByClassName('inp')[4].value = ''
    } else {
        document.getElementsByClassName('inp')[4].style.display = 'none'
        document.getElementsByClassName('inp')[4].value = e.value
    }
}))


const inpData = document.getElementById('data')
const inpTempo = document.getElementById('tempo')
window.onload = () => {
    const dataAtual = new Date();
    const data = dataAtual.toLocaleDateString();
    const [dia, mes, ano] = data.split("/");

    let hora = `${dataAtual.getHours()}`
    let min = `${dataAtual.getMinutes()}`
    inpData.value = `${ano}-${mes}-${dia}`;
    inpTempo.value = `${hora.padStart(2, "0")}:${min.padStart(2, "0")}`
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
let cod = false
const container = document.getElementsByClassName('container')
async function teste() {
    cod = !cod

    if (cod) {
        container[0].style.transform = `translateX(-104%)`
        await delay(1000)
        container[0].style.display = 'none'
        container[1].style.display = 'grid'
        await delay(100)
        container[1].style.transform = `translateY(0)`
        container[1].style.opacity = 1
        await delay(300)
        container[1].classList.add('anima-menu')
        document.getElementById('title-menu').style.display = 'block'
        document.getElementById('title-menu').style.opacity = 1
    } else {
        container[1].style.transform = `translateY(-104%)`
        container[1].style.opacity = 0
        await delay(1000)
        container[0].style.display = 'block'
        container[1].style.display = 'none'
        document.getElementById('title-menu').style.display = 'none'
        await delay(100)
        container[0].style.transform = `translateX(0)`
        container[1].classList.remove('anima-menu')
    }
}