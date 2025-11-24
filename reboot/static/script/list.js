// funções globais
let bd_authLista
let authLista
let statusLista
let dataAtual = new Date();

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const selectMes = document.getElementById("selectMes");
const selectAno = document.getElementById("selectAno");
const cenario = document.querySelectorAll('.radio-item')

async function filtroItens() {
    authLista = bd_authLista

    cenario.forEach(i => {
        if (i.checked && parseInt(i.value) != 0) {
            let cod = statusLista.filter(e => e[2] == parseInt(i.value)).map(e => e[1])
            authLista = authLista.filter(item => cod.includes(item[0]));
        }
    })

    printar(authLista)

    if (autoridade != 2) {
        const resultMap = {};
        for (const item of bd_authLista) {
            const nome = item[2][1];
            const caso = item[1];
            const curso = item[9];

            const chave = `${nome}-${curso}-${caso}`;

            if (!resultMap[chave]) {
                resultMap[chave] = {
                    nome,
                    curso,
                    caso,
                    quantidade: 0
                };
            }

            resultMap[chave].quantidade++;
        }

        let newList = Object.values(resultMap).map(obj => [
            obj.nome,
            obj.curso,
            obj.caso,
            obj.quantidade
        ]);

        newList = newList.filter(item => item[3] >= 3);

        const btn = document.getElementsByClassName('alert-qnt')[0]
        const ul = document.getElementsByClassName('lista-alert')[0]
        ul.innerHTML = ''
        if (newList.length) {
            await delay(100)
            btn.style.display = 'flex'
            newList.forEach(item => {
                const li = document.createElement("li");
                li.innerHTML = `<div><p><u>${item[0]}</u></p><p>curso: ${item[1]}</p><p>solicitação: ${item[2]}</p><p><b>quantidade: ${item[3]}</b></p></div>`;
                ul.appendChild(li);
            });

        } else {
            btn.style.display = 'none'
        }
    }
}

function formatoHora(e) {
    const partes = e.split(":");
    let horas = partes[0].padStart(2, '0');
    let minutos = partes[1].padStart(2, '0');
    let segundos = partes[2] ? partes[2].padStart(2, '0') : "00";
    return `${horas}:${minutos}:${segundos}`
}

// aviso dos alunos forgados
const btn = document.getElementsByClassName('alert-qnt')[0]
const box = document.getElementsByClassName('alert-qnt-box')[0]

function abrirLista() {
    btn.classList.remove('fechar-alert')
    box.classList.remove('fechar-alert-box')
    btn.classList.add('abrir-alert')
    box.classList.add('abrir-alert-box')
    document.getElementById('sair-maior').style.display = 'block'
}
function fecharLista() {
    btn.classList.remove('abrir-alert')
    box.classList.remove('abrir-alert-box')
    btn.classList.add('fechar-alert')
    box.classList.add('fechar-alert-box')
    document.getElementById('sair-maior').style.display = 'none'
}

// configuração do curso

function dellCurso(id) {
    const resposta = confirm(`Se continuar, todos os registros salvos nesse curso será desativado.`);

    if (resposta) {
        fetch(`/deletando-curso/${id}`)
            .then(res => {
                if (res.redirected) {
                    window.location.href = res.url;
                } else {
                    alert("Erro ao deletar.");
                }
            });
    }
}

const inp = document.getElementById('inp')
const title = document.getElementById('title')

const boxtitle = document.getElementsByClassName('box-title')[0]
const boxedit = document.getElementsByClassName('edit-curso')[0]

function openEdit() {
    boxtitle.style.display = 'none'
    boxedit.style.display = 'flex'
    inp.value = title.textContent
}

function closeEdit() {
    boxtitle.style.display = 'flex'
    boxedit.style.display = 'none'
}

//modal

const modal = document.getElementsByClassName('modal')[0]
const boxModal = document.getElementsByClassName('box-modal')[0]
const modalAlert = document.getElementsByClassName('modal-alert')[0]
const boxModalAlert = document.getElementsByClassName('modal-alert-box')[0]
function abrirModal(i = 0) {
    if (i == 1) {
        modalAlert.classList.add('abrir-modal')
        modalAlert.classList.remove('fechar-modal')
        boxModalAlert.classList.add('abrir-boxModal')
        boxModalAlert.classList.remove('fechar-boxModal')
        return
    }
    modal.classList.add('abrir-modal')
    modal.classList.remove('fechar-modal')
    boxModal.classList.add('abrir-boxModal')
    boxModal.classList.remove('fechar-boxModal')
}
function getAuth(id) {
    const statusAluno = statusLista.find(u => u[1] === id)
    if (`${statusAluno[5]}`.length != 7 && statusAluno[5]!=3) {
        abrirModal()
        document.getElementsByClassName('radio2')[0].checked = true
        document.getElementsByClassName('radio2')[1] = false
        select(0)


        let aluno = authLista.find(u => u[0] === id)
        registros(statusAluno, aluno[8], aluno[1], aluno[2][1], statusAluno[5])

        textoModal(id)
        chek.innerHTML = `
        <input type="checkbox" onclick="visto(${curso},${statusAluno[0]})" id="checkboxInput">
        <label for="checkboxInput" class="toggleSwitch"></label>
    `
        document.getElementsByClassName('info-auth')[0].style.display = 'block'
        document.getElementsByClassName('nav-modal')[0].style.display = 'none'
        document.getElementsByClassName('cod-modal')[0].style.display = 'none'

        const checkbox = document.getElementById('checkboxInput')
        const msgChek = document.getElementById('msg-check')
        const spanChek = document.getElementById('chek')
        switch (autoridade) {
            case 3:
                document.getElementsByClassName('nav-modal')[0].style.display = 'flex'
                msgChek.innerHTML = '<b>marcar como Aprovado?</b>'
                if (statusAluno[7]) {
                    checkbox.checked = true
                }
                document.getElementsByClassName('cod-modal')[0].style.display = 'flex'
                break;
            default:
                if (statusAluno[7]) {
                    msgChek.innerHTML = '<b>marcar como Ação Concluída?</b>'
                    spanChek.style.display = 'flex'
                    if (statusAluno[6]) {
                        checkbox.checked = true
                    }
                } else {
                    msgChek.innerHTML = '<b>Esperando a aprovação da coordenação.</b>'
                    spanChek.style.display = 'none'
                }
                break;
        }
        if (aluno[1] == 'Saída' && autoridade == 2) {
            document.getElementsByClassName('cod-modal')[0].style.display = 'flex'
        } else if (aluno[1] == 'Entrada' && autoridade == 1) {
            document.getElementsByClassName('cod-modal')[0].style.display = 'flex'
        }
    }
}

function registros(status, docente, caso, aluno, cod) {
    function dataHora(dataOriginal) {
        if (!dataOriginal) {
            return false
        }
        const data = new Date(dataOriginal.replace(' ', 'T'));

        const dia = String(data.getDate()).padStart(2, '0');
        const mes = String(data.getMonth() + 1).padStart(2, '0');
        const ano = data.getFullYear();
        const hora = String(data.getHours()).padStart(2, '0');
        const minuto = String(data.getMinutes()).padStart(2, '0');

        return [`${dia}/${mes}/${ano}`, ` ${hora}:${minuto}`];
    }

    let funcao = docente[2] == 3 ? 'Coordenador(a)' : 'Professor(a)'

    const lista = [
        { acao: docente[2] == 3 ? "Autorizado e aprovado" : "Autorizado", usuario: docente, funcao: funcao, data: dataHora(status[10])[0], hora: dataHora(status[10])[1] },
        { acao: "Aprovado", usuario: status[4], funcao: 'coordenador(a)', data: dataHora(status[7])[0] || '', hora: dataHora(status[7])[1] || '' },
        { acao: "Confirmado", usuario: status[3][0] || '', funcao: status[3][1] ? status[3][1] == 1 ? 'Professor(a)' : 'Vigia' : '', data: dataHora(status[6])[0] || '', hora: dataHora(status[6])[1] || '' },
    ];
    let msg = ''
    if (dataHora(status[9])[0]) {
        if (dataHora(status[8])[0]) {
            msg = `<div class="info-dt-box"><p>• Responsável notificado</p> <span class="info-dt-btn">i<span class="info-dt"">${dataHora(status[8])[0]} às ${dataHora(status[8])[1]}</span></span></div><div class="info-dt-box"><p>Autorização confirmada via sistema.</p><span class="info-dt-btn">i<span class="info-dt"">${dataHora(status[9])[0]} às ${dataHora(status[9])[1]}</span></span></div>`
        } else {
            msg = `• Responsável não foi notificado. Liberação efetuada por fora do sistema, na data ${dataHora(status[9])[0]} às ${dataHora(status[9])[1]}`
        }
    } else if (cod == 2) {
        msg = `${dataHora(status[8])[0] ? `<div class="info-dt-box"><p>• Responsável notificado</p> <span class="info-dt-btn">i<span class="info-dt"">${dataHora(status[8])[0]} às ${dataHora(status[8])[1]}</span></span></div>` : '<div class="info-dt-box"><p>• Responsável não foi notificado via sistema</p></div>'}<div class="info-dt-box" style="color:red"><p>Saída de menor autorizada fora do sistema.</p></div>`
    } else {
        msg = dataHora(status[8])[0] ? `<div class="info-dt-box"><p>• Responsável notificado</p> <span class="info-dt-btn">i<span class="info-dt"">${dataHora(status[8])[0]} às ${dataHora(status[8])[1]}</span></span></div>` : '<div class="info-dt-box"><p>• Responsável não foi notificado via sistema</p></div>'
    }

    document.getElementById('msg-resp').innerHTML = msg

    const tbody = document.getElementsByClassName('table')[0];
    tbody.innerHTML = `
            <tr>
              <th>Ação</th>
              <th>Usuário</th>
              <th>Função</th>
              <th>Data</th>
              <th>Horário</th>
            </tr>`

    let cont = 0
    lista.forEach(usuario => {
        if (usuario.data && cont == 0) {
            const linha = document.createElement("tr");
            linha.innerHTML = `
            <td>${usuario.acao}</td>
            <td>${usuario.acao == 'Confirmado' ? usuario.usuario : usuario.usuario[1]}</td>
            <td>${usuario.funcao}</td>
            <td>${usuario.data}</td>
            <td>${usuario.hora}</td>
            `;
            tbody.appendChild(linha);
            if (lista[0].usuario[0] == lista[1].usuario[0]) {
                cont = 1
            }
        } else { cont = 0 }
    });

    const tbody2 = document.getElementsByClassName('table')[1];
    tbody2.innerHTML = ''

    const quantidadeMes = authLista.filter(item => {
        const [ano, mes] = item[4].split("-");
        let dt = [parseInt(ano), parseInt(mes)];

        if (item[2][1] === aluno && item[1] === caso) {
            if (dt[0] == selectAno.value) {
                if (dt[1] == selectMes.value) {
                    return item
                }
            }
        }
    }).length;
    const quantidadeAno = bd_authLista.filter(item => {
        const [ano] = item[4].split("-");
        let dt = [parseInt(ano)];
        if (item[2][1] === aluno && item[1] === caso) {
            if (dt[0] == selectAno.value) {
                return item
            }
        }
    }).length;

    document.getElementById('caso-title').textContent = caso

    const lista2 = [
        { tipo: 'do Mês', quant: quantidadeMes },
        { tipo: 'do Ano', quant: quantidadeAno },
    ]

    lista2.forEach(item => {
        const linha = document.createElement("tr");
        linha.innerHTML = `
            <td>${item.tipo}</td>
            <td>${item.quant}</td>
            `;
        tbody2.appendChild(linha);
    });
}

function verCod() {
    const chek2 = document.getElementById('chek2')
    if (chek2.checked) {
        let resposta = confirm("Solicitamos que confirme esta informação e esteja ciente da responsabilidade em relação à saída do(a) estudante.");
        if (resposta) {
            document.getElementById('cod').style.backgroundColor = 'white'
        } else {
            chek2.checked = false
        }
    } else {
        document.getElementById('cod').style.backgroundColor = 'black'
    }
}

function fecharModal(i = 0) {
    if (i == 1) {
        boxModalAlert.classList.remove('abrir-boxModal')
        boxModalAlert.classList.add('fechar-boxModal')
        modalAlert.classList.remove('abrir-modal')
        modalAlert.classList.add('fechar-modal')
        return
    }
    boxModal.classList.remove('abrir-boxModal')
    boxModal.classList.add('fechar-boxModal')
    modal.classList.remove('abrir-modal')
    modal.classList.add('fechar-modal')
}

const infoModal = document.querySelectorAll('.info-auth')
function select(i) {
    for (let e = 0; e < 2; e++) {
        infoModal[e].style.display = 'none'
    }

    infoModal[i].style.display = 'block'
    document.getElementById('title-modal').textContent = i == 0 ? 'Autorização' : 'Registros'
}

const obs = document.getElementById('obs-auth-modal')
const agenda = document.getElementsByClassName('inp-text')
function textoModal(id) {
    let aluno = authLista.find(u => u[0] === id)
    if (aluno[7]) {
        obs.style.display = 'block'
        obs.textContent = 'obs: ' + aluno[7]
    } else {
        obs.style.display = 'none'
        obs.textContent = ''
    }
    document.getElementById('docente').textContent = '• Docente » ' + aluno[8][1]
    document.getElementById('motivo').textContent = aluno[6]
    agenda[0].value = aluno[4]
    agenda[1].value = formatoHora(aluno[5])
    document.getElementById('curso').textContent = aluno[9]
    document.getElementById('atividade').textContent = aluno[3]
    document.getElementById('aluno').textContent = '➤ ' + aluno[2][1]
    document.getElementById('caso').textContent = aluno[1]
}

async function visto(id, id_status) {
    const checkbox = document.getElementById('checkboxInput')
    if (!checkbox.checked) {
        checkbox.checked = true
        return
    }
    await delay(200)
    try {
        const res = await fetch(`/visto/${id ? id : 0}/${id_status}`);
        const data = await res.json();
        window.location.href = data.redirect_url;
    } catch (error) {
        console.error('Erro ao chamar a API:', error);
    }
}

//construindo a lista de autorizações
const container = document.getElementsByClassName('container')[0]
const chek = document.getElementById('chek')
function printar(lista) {
    container.innerHTML = ''

    if (!lista.length) {
        container.innerHTML = '<h3>Nenhuma solicitação foi encontrada...</h3>'
        return
    }

    lista.slice().reverse().forEach(e => {
        const statusAluno = statusLista.find(u => u[1] === e[0])

        const partes = e[5].split(":");

        let horas = partes[0].padStart(2, '0');
        let minutos = partes[1].padStart(2, '0');
        let segundos = partes[2] ? partes[2].padStart(2, '0') : "00";

        let horario = `${horas}:${minutos}:${segundos}`;

        container.innerHTML += `
        <div class="item" onclick="getAuth(${e[0]})" style="${`${statusAluno[5]}`.length == 7 || statusAluno[5]==3? 'background-color:rgba(255, 50, 43, 1)' : 'cursor: pointer;'}">
            <div class="boxPreview">
            <img class="imagePreview" src="${`/imagem/${e[2][0]}` ? `/imagem/${e[2][0]}` : '../static/img/user.svg'}" alt="foto-do-aluno(a)">
            <p class="cenario-item"
            style="background-color: ${statusAluno[5]==3?'rgba(255, 0, 0, 0.5)':statusAluno[2] == 1 ? 'rgba(0, 0, 255, 0.5)' : statusAluno[2] == 2 ? 'rgba(0, 255, 0, 0.5)' : 'rgba(255, 170, 0, 0.8)'};color:white;"
            >
            <b>${statusAluno[5]==3?'Negado':statusAluno[2] == 1 ? 'Em espera' : statusAluno[2] == 2 ? 'ação confirmada' : 'ação pendente'}</b>
            </p>
            </div>
            <div class="boxInfo" style="display:flex;">
            <div>
            ${`${statusAluno[5]}`.length == 7  || statusAluno[5]==3? `
                <h2 style="color:white;text-align: center;margin-bottom:5px;">${statusAluno[5]!=3?'Esperando autorização do responsável':'Responsável não autorizou'}</h2>
                <h3 style="background-color:rgba(255,255,255); border-radius:5px;margin:auto; padding:0 3px;">Aluno: ${e[2][1]}</h3>
            `: `
            </div>
            <div class="boxInfo" style="flex:3;">
            <h2 style="text-align: center; color:#333"><u>${e[1]}</u></h2>
            <h3 style="margin:5px 0">${e[2][1]}</h3>
            <input type="date" class="inp-text" value="${e[4]}" readonly>
            <input type="time" class="inp-text" value="${horario}" readonly>
            </div>
            <div class="boxStatus">
            <p>${statusAluno[8] ? '<img src="../static/img/pai.svg" alt="Responsável" width="30px">' : ''}</p>
            <p>${statusAluno[7] ? '<img src="../static/img/homem.svg" alt="Coordenador" width="30px">' : ''}</p>
            <p>${statusAluno[3][1] == 1 && statusAluno[3] ? statusAluno[6] ? '👨‍🏫' : '' : statusAluno[6] ? '🛡️' : ''}</p>
            </div>
            </div>
            ${statusAluno[8] || statusAluno[7] || statusAluno[6] ?
                `
            <div class="boxStatus-info">
            <p>${statusAluno[8] ? statusAluno[9] ? '➔ Responsável notificado, e autorização confirmada' : '➔ Responsável notificado' : ''}</p>
            <p>${statusAluno[9] ? '➔ Autorizado pelo responsável' : ''}</p>
            <p>${statusAluno[7] ? '➔ Aprovado pela coordenação' : ''}</p>
            <p>${statusAluno[3][1] == 1 && statusAluno[3] ? statusAluno[6] ? '➔ Visto pelo professor(a)' : '' : statusAluno[6] ? '➔ Visto pelo guarita' : ''}</p>
            </div>
                `
                : ''}
            `}
        </div>
    `
    })
}

async function loadItems() {
    const API_URL = `/get-items${curso ? "/" + curso : ''}?dt=${[selectMes.value, selectAno.value]}`;

    const res = await fetch(API_URL);
    const [items, status] = await res.json();
    authLista = JSON.parse(items)
    bd_authLista = authLista
    statusLista = JSON.parse(status)
    filtroItens()
    setTimeout(loadItems, 10000);
}
async function loading() {
    await loadItems();
    if (id != 0) {
        await getAuth(parseInt(id));
    }
}
function loadingPage() {
    selectMes.value = dataAtual.getMonth() + 1;
    for (let i = 0; i < dataAtual.getFullYear() - 2024; i++) {
        const novaOpcao = document.createElement("option");
        novaOpcao.value = dataAtual.getFullYear() - i;
        novaOpcao.textContent = dataAtual.getFullYear() - i;
        selectAno.appendChild(novaOpcao);
    }
    loading()
}
loadingPage()