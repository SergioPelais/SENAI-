const input = document.getElementsByClassName('inp')

// determinado o tipo de caso do aluno (saida/entrada)
const at = document.getElementById('atividade')
at.value = 'Saída'
function opcao(num = 0) {
    at.value = num
    msgNotificar()
}

// trabalhando com atalho no campo 'motivos'
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
        input[4].style.display = 'block'
        input[4].value = ''
    } else {
        input[4].style.display = 'none'
        input[4].value = e.value
    }
}))

const boxEmail = document.getElementsByClassName('box-email')[0]
// aplicando data e hora atual no formulário
const inpData = document.getElementById('data')
const inpTempo = document.getElementById('tempo')
const dataAtual = new Date();
window.onload = () => {
    const data = dataAtual.toLocaleDateString();
    const [dia, mes, ano] = data.split("/");

    let hora = `${dataAtual.getHours()}`
    let min = `${dataAtual.getMinutes()}`
    inpData.value = `${ano}-${mes}-${dia}`;
    inpTempo.value = `${hora.padStart(2, "0")}:${min.padStart(2, "0")}`
}

// transição de formulário, para, Menu
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

// buscando aluno
const estado = document.getElementById('estado') //serve para definir se o anulo é de menor para comunicacao com py
const listaAlunos = bd
const ul = document.getElementById('resultados');
let resultadoAluno = ''
input[0].addEventListener('input', function () {
    const termo = this.value.toLowerCase();

    if (termo.trim()) {
        const resultados = listaAlunos.filter(aluno =>
            aluno[1].toLowerCase().includes(termo)
        );
        resultadoAluno = resultados[0]
        mostrarResultados(resultados);
    } else {
        ul.innerHTML = '';
    }


});
function mostrarResultados(lista) {
    ul.innerHTML = '';
    ul.style.color = 'black'
    lista.forEach(aluno => {
        ul.innerHTML += `<li onclick="atalho2(${aluno[0]})">• ${aluno[1]}</li>`
    });
}

function atalho2(i) {
    resultadoAluno = listaAlunos[i - 1]
}

const idAluno = document.getElementById('id-aluno')
input[0].addEventListener('blur', async function () {
    const termo = this.value.toLowerCase();
    if (termo.trim()) {
        if (resultadoAluno) {
            await delay(300)
            ul.innerHTML = 'Aluno encontrado com sucesso!';
            ul.style.color = 'green'
            input[0].value = resultadoAluno[1]
            input[5].value = resultadoAluno[4]
            input[6].value = resultadoAluno[5]
            idAluno.value = resultadoAluno[0]
            notificar()
            return

        } else {
            ul.innerHTML = 'Aluno não encontrado...';
            ul.style.color = 'red'
        }

    }
    idAluno.value = 'none'
    boxEmail.style.display = 'none'
    input[6].value = ''
    input[5].value = ''
    ul.innerHTML = '';
})

//tratamento de notificação ao responsavel
const msgCaso = document.getElementById('msg-caso')
function notificar() {
    const [ano, mes, dia] = resultadoAluno[2].split("-");
    if (dataAtual.getFullYear() - ano >= 18) {
        if (dataAtual.getDate() >= dia && dataAtual.getMonth() + 1 >= mes) {
            estado.value = false
            boxEmail.style.display = 'none'
            return
        }
    }
    estado.value = true
    boxEmail.style.display = 'block'
    msgNotificar()
}

const checkbox = document.getElementById('check-box')
function msgNotificar() {
    msgCaso.textContent = `Um email para o responsavel será enviado, notificando sobre a '${at.value}' fora do horário padrão.`
    if (at.value === 'Saída') {
        checkbox.style.display = 'block'
    } else {
        checkbox.style.display = 'none'
    }
}


