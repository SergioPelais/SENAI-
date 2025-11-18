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

    if (e.value == tags[3]) {
        input[3].style.display = 'block'
        input[3].value = ''
    } else {
        input[3].style.display = 'none'
        input[3].value = e.value
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
const fundo = document.getElementsByClassName('fundo')[0]

if (menu[0] == '1') {
    cod = true
    teste2()
} else {
    cod = false
    teste3(menu[1] != 1 ? 1 : 0)
}

async function teste2() {
    container[1].style.transform = `translateY(0)`
    container[0].style.transform = `translateX(-115%)`
    container[0].style.display = 'none'
    container[1].style.display = 'flex'
    await delay(100)
    container[1].style.opacity = 1
    for (let i = 1; i < 100; i++) {
        await delay(0.5)
        fundo.style.background = `linear-gradient(${45 + i}deg, rgba(255, 40, 40, ${0.8 - i * 0.01 > 0.3 ? 0.8 - i * 0.01 : 0.3}), rgba(144, 51, 161, ${0.3 - i * 0.1 > 0.1 ? 0.3 - i * 0.1 : 0.1}), white)`
    }

}
async function teste3(ativo = 0) {
    container[0].style.transform = `translateX(-115%)`
    if (ativo == 1) { container[0].style.transform = `translateX(0)` }
    container[0].style.display = 'block'
    container[1].style.display = 'none'
    await delay(100)
    container[0].style.transform = `translateX(0)`
    for (let i = 1; i < 100; i++) {
        await delay(0.5)
        fundo.style.background = `linear-gradient(${145 - i}deg, rgba(255, 40, 40, ${0.3 + i * 0.01 < 0.8 ? 0.3 + i * 0.01 : 0.8}), rgba(144, 51, 161, ${0.1 + i * 0.1 < 0.3 ? 0.1 + i * 0.1 : 0.3}), white)`
    }
}
async function teste() {
    cod = !cod

    if (cod) {
        container[0].style.transform = `translateX(-115%)`
        await delay(1000)
        container[0].style.display = 'none'
        container[1].style.display = 'flex'
        await delay(100)
        container[1].style.transform = `translateY(0)`
        container[1].style.opacity = 1
        for (let i = 1; i < 100; i++) {
            await delay(0.5)
            fundo.style.background = `linear-gradient(${45 + i}deg, rgba(255, 40, 40, ${0.8 - i * 0.01 > 0.3 ? 0.8 - i * 0.01 : 0.3}), rgba(144, 51, 161, ${0.3 - i * 0.1 > 0.1 ? 0.3 - i * 0.1 : 0.1}), white)`
        }
    } else {
        container[1].style.transform = `translateY(-104%)`
        container[1].style.opacity = 0
        await delay(500)
        container[0].style.display = 'block'
        container[1].style.display = 'none'
        await delay(100)
        container[0].style.transform = `translateX(0)`
        for (let i = 1; i < 100; i++) {
            await delay(0.5)
            fundo.style.background = `linear-gradient(${145 - i}deg, rgba(255, 40, 40, ${0.3 + i * 0.01 < 0.8 ? 0.3 + i * 0.01 : 0.8}), rgba(144, 51, 161, ${0.1 + i * 0.1 < 0.3 ? 0.1 + i * 0.1 : 0.3}), white)`
        }
    }
}

// buscando aluno
const estado = document.getElementById('estado') //serve para definir se o aluno é de menor para comunicacao com py
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
    resultadoAluno = listaAlunos.find(u => u[0] === i);
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
            idAluno.value = resultadoAluno[0]
            notificar()
            return

        } else {
            ul.innerHTML = 'Aluno não encontrado...';
            ul.style.color = 'red'
            input[5].value = ''
            input[4].value = ''
        }
    } else { ul.innerHTML = ''; }
    idAluno.value = 'none'
    boxEmail.style.display = 'none'
    input[5].value = ''
    input[4].value = ''

})

//tratamento de notificação ao responsavel, ou, verificando se o aluno é de maior
const msgCaso = document.getElementById('msg-caso')
function notificar() {
    const [ano, mes, dia] = resultadoAluno[2].split("-");
    let idade = 0

    if (dataAtual.getMonth() + 1 >= mes) {
        if (dataAtual.getDate() >= dia || dataAtual.getMonth() + 1 > mes) {
            idade = dataAtual.getFullYear() - ano
        }
    } else { idade = (dataAtual.getFullYear() - ano) - 1 }

    if (idade >= 18) {
        estado.value = false
        document.getElementById('chek').checked = false
    } else {
        document.getElementById('chek').checked = true
        estado.value = true
    }
    document.getElementById('email-print').textContent = resultadoAluno[3]
    document.getElementById('tell-print').textContent = resultadoAluno[4]
    input[4].value = resultadoAluno[3]
    input[5].value = resultadoAluno[4]
    boxEmail.style.display = 'block'
    msgNotificar()
}

const checkbox = document.getElementById('check-box')
function msgNotificar() {
    msgCaso.textContent = `Um email para o responsavel será enviado, notificando sobre a '${at.value}' fora do horário padrão.`

    if (at.value === 'Saída' && estado.value == 'true') {
        checkbox.style.display = 'block'
    } else {
        checkbox.style.display = 'none'
    }
}

function verificar() {
    let check = document.getElementById('chek')
    if (!check.checked) {
        const resposta = confirm(`Ao desmarcar, espera-se que o responsável já tenha autorizado por fora do sistema.\nDeseja continuar?`);
        if(resposta){
            check.checked = false
            return
        }
    }
    check.checked = true
}