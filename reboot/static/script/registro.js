const curso = data
const auth_alunos = data_auth
const auth_alunos_status = data_status

const edit = document.getElementById('edit')
const noneDiv = document.getElementsByClassName('none')[0]
const boxEdit = document.getElementsByClassName('box-edit')[0]
const inp = document.getElementsByClassName('inp')[0]

function editar() {
    noneDiv.style.display = 'none'
    boxEdit.style.display = 'flex'
    inp.placeholder = `${curso[1]} | digite aqui o novo nome do curso`
}
function cancel() {
    noneDiv.style.display = 'block'
    boxEdit.style.display = 'none'
    inp.value = ''
}

function perguntar() {
    const resposta = confirm(`Deseja continuar?\n*Se continuar tudo relacionando ao curso '${curso[1]}' não será mais listado!`);

    if (resposta) {
        fetch(`/deletando-curso/${curso[0]}`)
            .then(res => res.json())
            .then(data => {
                window.location.href = data.redirect_url;
            });
    }
}

const modal = document.getElementsByClassName('modal')[0]
const boxModal = document.getElementsByClassName('modal-box')[0]
function abrirModal(id = 1) {
    boxModal.classList.remove('fechar2')
    boxModal.classList.add('abrir2')

    modal.classList.add('abrir')
    modal.classList.remove('fechar')


    let auth = auth_alunos.find(u => u[0] === id);
    document.getElementById('caso').textContent = auth[1]
    document.getElementById("imagePreview").src = '/imagem/' + auth[2][0]
    document.getElementsByClassName('info-modal')[0].innerHTML = `
        <div style="flex: 3;">
            <h3>Aluno(a): ${auth[2][1]}</h3>
            <div style="padding: 10px 20px;">
                <p>Atividade ➜ ${auth[3]}</p>
                <p>Curso: ${curso[1]}</p>
                <div class="time-modal">
                    <input type="date" class="inp-text" value="${auth[4]}" readonly>
                    <input type="time" class="inp-text" value="${auth[5]}" readonly>
                </div>
                <p>• Motivo: ${auth[6]}</p>
                ${auth[7].trim() ? `
                <div class="obs">
                    <p><b>Observação:</b></p>
                    <p>${auth[7]}</p>
                </div>
                    `: ''}
            </div>
            <h3>Docente: ${auth[8]}</h3>
        </div>
    `
    let status = auth_alunos_status.find(u => u[1] === auth[0]);

    document.getElementsByClassName("visto")[0].innerHTML = `
        <p>marcar como visto?</p>
        <!-- From Uiverse.io by vinodjangid07 -->
        <input type="checkbox" id="checkboxInput" ${status[2] === 2 ? 'checked' : ''}>
        <label for="checkboxInput" class="toggleSwitch" onclick="visto(${status[0]})"></label>
    `
}
function fecharModal() {
    modal.classList.remove('abrir')
    modal.classList.add('fechar')
    boxModal.classList.add('fechar2')
}

const container = document.getElementsByClassName('container')[0]

function printar() {
    container.innerHTML = ''

    auth_alunos.slice().reverse().forEach(e => {
        let status = auth_alunos_status.find(u => u[1] === e[0]);

        let msg = ''
        let cor = '#555'

        switch (status[2]) {
            case 1:
                msg = 'Ação: em espera'
                cor = 'blue'
                break;
            case 2:
                msg = 'Ação: confirmada'
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
            default:
                break;
        }

        const partes = e[5].split(":");

        let horas = partes[0].padStart(2, '0');
        let minutos = partes[1].padStart(2, '0');
        let segundos = partes[2] ? partes[2].padStart(2, '0') : "00";

        let horario = `${horas}:${minutos}:${segundos}`;

        container.innerHTML += `
        <div class="item" onclick="abrirModal(${e[0]})">
            <div class="item-content" style="border: none">
            <h2 style="text-align: center; color:#333"><u>${e[1]}</u></h2>
            <h3 style="margin:5px 0">${e[2][1]}</h3>
            <input type="date" class="inp-text" value="${e[4]}" readonly>
            <input type="time" class="inp-text" value="${horario}" readonly>
            </div>
            <div class="item-info">
            <p style='color:${cor}'>${msg}</p>
            <p style='color:#555'>${status[3] ? 'visto por ' + status[3] : ''}</p>
            </div>
        </div>
    `
    })
}
printar()

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
async function visto(id) {
    const checkbox = document.querySelector('#checkboxInput')
    let ativo = 4
    if (!checkbox.checked) {
        ativo = 2
    }

    await delay(200)
    try {
        const res = await fetch(`/visto/${curso[0]}/${id}/${ativo}`, { method: 'POST' });
        const data = await res.json();
        window.location.href = data.redirect_url;
    } catch (error) {
        console.error('Erro ao chamar a API:', error);
    }
}