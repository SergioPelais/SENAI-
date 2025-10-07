const curso = data
const auth_alunos = data_auth

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
function abrirModal(){
    boxModal.classList.remove('fechar2')
    boxModal.classList.add('abrir2')
    
    modal.classList.add('abrir')
    modal.classList.remove('fechar')
}
function fecharModal(){
    modal.classList.remove('abrir')
    modal.classList.add('fechar')
    boxModal.classList.add('fechar2')
}

const container = document.getElementsByClassName('container')[0]

function printar(){
    container.innerHTML = ''
    
    container.innerHTML += `
        <div class="item" onclick="abrirModal()">
            <h2 style="text-align: center;">Entrada</h2>
            <h3>Carlos gabriel dos santos araujo</h3>
            <p>Horário: 09:27</p>
            <p>Data: 05-01-2007</p>
        </div>
                    <div class="item" onclick="abrirModal()">
                <h2 style="text-align: center;">Entrada</h2>
                <h3>Carlos gabriel dos santos araujo</h3>
                <p>Horário: 09:27</p>
                <p>Data: 05-01-2007</p>
            </div>
            <div class="item" onclick="abrirModal()">
                <h2 style="text-align: center;">Entrada</h2>
                <h3>Carlos gabriel dos santos araujo</h3>
                <p>Horário: 09:27</p>
                <p>Data: 05-01-2007</p>
            </div>
            <div class="item" onclick="abrirModal()">
                <h2 style="text-align: center;">Entrada</h2>
                <h3>Carlos gabriel dos santos araujo</h3>
                <p>Horário: 09:27</p>
                <p>Data: 05-01-2007</p>
            </div>
            <div class="item" onclick="abrirModal()">
                <h2 style="text-align: center;">Entrada</h2>
                <h3>Carlos gabriel dos santos araujo</h3>
                <p>Horário: 09:27</p>
                <p>Data: 05-01-2007</p>
            </div>
    `
}
printar()