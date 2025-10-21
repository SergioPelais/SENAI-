const auth_alunos = data_auth
const auth_alunos_status = data_status

const edit = document.getElementById('edit')
const noneDiv = document.getElementsByClassName('none')[0]
const boxEdit = document.getElementsByClassName('box-edit')[0]
const inp = document.getElementsByClassName('inp')[0]



const modal = document.getElementsByClassName('modal')
const boxModal = document.getElementsByClassName('modal-box')[0]
const modal1 = document.getElementsByClassName('none-primary')[0]
const modal2 = document.getElementsByClassName('none-secondary')[0]
function abrirModal(id = 1) {
    boxModal.classList.remove('fechar2')
    boxModal.classList.add('abrir2')

    let auth = auth_alunos.find(u => u[0] === id);
    document.getElementById('caso').textContent = auth[1]
    document.getElementById("imagePreview").src = '/imagem/' + auth[2][0]
    document.getElementsByClassName('info-modal')[0].innerHTML = `
        <div style="flex: 3;">
            <h3>Aluno(a): ${auth[2][1]}</h3>
            <div style="padding: 10px 20px;">
                <p style="${autoridade==2?'display: none;':''}">Atividade ➜ ${auth[3]}</p>
                <p style="${autoridade==2?'display: none;':''}">Curso: ${auth[9][1]}</p>
                <div class="time-modal">
                    <input type="date" class="inp-text" value="${auth[4]}" readonly>
                    <input type="time" class="inp-text" value="${auth[5]}" readonly>
                </div>
                <p style="${autoridade==2?'display: none;':''}">• Motivo: ${auth[6]}</p>
                ${auth[7].trim() ? `
                <div class="obs" style="${autoridade==2?'display: none;':''}">
                    <p><b>Observação:</b></p>
                    <p>${auth[7]}</p>
                </div>
                    `: ''}
            </div>
            <h3 style="${autoridade==2?'display: none;':''}">Docente: ${auth[8]}</h3>
        </div>
        <p style="color:green;font-weight:bold;border:2px solid rgb(150,255,150);padding:3px" id="resp-box"></p>
    `
    let status = auth_alunos_status.find(u => u[1] === auth[0]);
    document.getElementById('resp-box').textContent = status[5]?status[5] == 1?"autorizado pelo responsável":"responsável notificado":""
    document.getElementById('resp-box').style.display = status[5]? 'block':'none'
    if(status[5] && String(status[5]).length == 7){
        modal1.style.display = 'none'
        modal2.style.display = 'block'
        modal[1].classList.add('abrir')
        modal[1].classList.remove('fechar')
    }else{
        modal2.style.display = 'none'
        modal1.style.display = 'block'
        modal[0].classList.add('abrir')
        modal[0].classList.remove('fechar')
    }
    document.getElementById('id-status').value = status[0]

    document.getElementsByClassName("visto")[0].innerHTML = `
        <p>marcar como ${autoridade == 2 ? 'visto' : 'aprovado'}?</p>
        <input type="checkbox" id="checkboxInput" ${status[2] === 2 && autoridade == 2 ? 'checked' : ''}>
        <label for="checkboxInput" class="toggleSwitch" onclick="visto(${status[0]},${auth[9][0]})"></label>
    `
    if (status[4] && autoridade == 3 && status[7]) {
        const dataISO = status[7].replace(" ", "T");

        const data = new Date(dataISO);

        const dia = String(data.getDate()).padStart(2, '0');
        const mes = String(data.getMonth() + 1).padStart(2, '0');
        const ano = data.getFullYear();

        const hora = String(data.getHours()).padStart(2, '0');
        const minutos = String(data.getMinutes()).padStart(2, '0');

        document.getElementsByClassName("visto")[0].innerHTML = `<p>Aprovado pelo coordenador(a) "${status[4]}", em ${dia}/${mes}/${ano} às ${hora}:${minutos}  </p>`
    }
}
function fecharModal() {
    modal[0].classList.remove('abrir')
    modal[0].classList.add('fechar')
    modal[1].classList.remove('abrir')
    modal[1].classList.add('fechar')
    boxModal.classList.add('fechar2')
}

if(id_modal){
    abrirModal(parseInt(id_modal))
}

const container = document.getElementsByClassName('container')[0]

function printar(lista) {
    container.innerHTML = ''

    if(autoridade==2){
        auth_alunos_status.forEach(e=>{
            if(e[2]==5){
                lista = lista.filter(i=>i[0]!=e[1])
            }
        }) 
    }

    lista.slice().reverse().forEach(e => {
        let status = auth_alunos_status.find(u => u[1] === e[0]);

        let msg = ''
        let cor = '#555'

        switch (status[2]) {
            case 1:
                msg = 'Ação: em espera'
                cor = 'blue'
                break;
            case 2:
                msg = 'Ação: confirmado'
                cor = 'green'
                break;
            case 3:
                msg = 'Ação: pendente'
                cor = 'orange'
                break;
            case 4:
                msg = 'Ação: Negada'
                cor = 'red'
                break;
            case 5:
                msg = 'Esperando confirmação do responsável'
                cor = 'red'
                break;
            default:
                break;
        }

        const partes = e[5].split(":");

        let horas = partes[0].padStart(2, '0');
        let minutos = partes[1].padStart(2, '0');
        let segundos = partes[2] ? partes[2].padStart(2, '0') : "00";

        let horario = `${horas}:${minutos}:${segundos}`;
        let genda = ''
        if(status[6]){
        const dataISO = status[6].replace(" ", "T");
        const data = new Date(dataISO);
        const dia = String(data.getDate()).padStart(2, '0');
        const mes = String(data.getMonth() + 1).padStart(2, '0');
        const ano = data.getFullYear();
        const hora = String(data.getHours()).padStart(2, '0');
        const min = String(data.getMinutes()).padStart(2, '0');
        genda = `, em ${dia}/${mes}/${ano} às ${hora}:${min}`
        }
        container.innerHTML += `
        <div class="item" onclick="abrirModal(${e[0]})">
            <div class="item-content" style="border: none">
            <h2 style="text-align: center; color:#333"><u>${e[1]}</u></h2>
            <h3 style="margin:5px 0">${e[2][1]}</h3>
            <input type="date" class="inp-text" value="${e[4]}" readonly>
            <input type="time" class="inp-text" value="${horario}" readonly>
            </div>
            <div class="item-info">
            <p style='color:${cor}'>${msg} - (${status[3] ? status[3] : '...'})${genda}</p>
            <p style='color:#444' id='none-text'>${status[4] && status[2] != 5  ? 'aprovado pela coordenação': ''}</p>
            </div>
        </div>
    `
    })
}
printar(auth_alunos)

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
async function visto(id,id_curso) {
    const checkbox = document.querySelector('#checkboxInput')
    let ativo = 3
    if (!checkbox.checked) {
        ativo = 2
    }

    await delay(200)
    try {
        const res = await fetch(`/visto/0/${id}/${ativo}`, { method: 'POST' });
        const data = await res.json();
        window.location.href = data.redirect_url;
    } catch (error) {
        console.error('Erro ao chamar a API:', error);
    }
}

const opc = document.querySelectorAll('.customCheckBoxInput')
let novalista = []
opc.forEach(i => i.addEventListener('click', () => {
    let lista = auth_alunos_status.filter(e => {
        if (e[2] == i.value) {
            return auth_alunos.find(u => u[0] === e[1]);
        }

    })

    if (i.checked) {
        if (lista.length) {
            novalista.push([parseInt(i.value), lista])
        }
    } else {
        novalista = novalista.filter(a => a[0] != parseInt(i.value))
    }

    let ids = novalista.flatMap(i => i[1].map(e => e[1]))

    let resultado = auth_alunos.filter(item => ids.includes(item[0]));
    
    if(resultado.length){
    printar(resultado)
    }else{
    printar(auth_alunos)
    }
}))

async function limpar(id) {
    try {
        const res = await fetch(`/limpar`, { method: 'POST' });
        const data = await res.json();
        window.location.href = data.redirect_url;
    } catch (error) {
        console.error('Erro ao chamar a API:', error);
    }
}