const input = document.getElementById('imageInput');
const preview = document.getElementById('imagePreview');

input.addEventListener('change', function () {
    const file = this.files[0];

    if (file) {
        const reader = new FileReader();

        reader.addEventListener('load', function () {
            preview.setAttribute('src', this.result);
        });

        reader.readAsDataURL(file);
    } else {
        preview.setAttribute('src', '../static/img/user.svg');
    }
});

const alunos = bd
const ul = document.getElementById('lista')
const inpBusca = document.getElementsByClassName('inp-busca')[0]
inpBusca.addEventListener('input', function () {
    const termo = this.value.toLowerCase();

    if (termo.trim()) {
        const resultados = alunos.filter(aluno =>
            aluno[1].toLowerCase().includes(termo)
        );
        printAlunos(resultados)
    } else {
        printAlunos(alunos)
    }
});

function printAlunos(lista) {
    ul.innerHTML = '';
    ul.style.color = 'black'
    lista.forEach(aluno => {
        ul.innerHTML += `<li>
        <a href="/alunos/${aluno[0]}">
        ${aluno[1]}</a>
        <button id="keep" onclick="dellAluno(${aluno[0]})">
            <img src="../static/img/delete.svg" width="40px" alt="notification">
        </button></li>`
    });
}

function dellAluno(id) {
    let aluno = alunos.find(u => u[0] === id);
    const resposta = confirm(`Deseja desativar o/a aluno/a '${aluno[1]}' ?`);

    if (resposta) {
        fetch(`/deletando-aluno/${aluno[0]}`)
            .then(res => {
                if (res.redirected) {
                    window.location.href = res.url;
                } else {
                    alert("Erro ao deletar.");
                }
            });
    }
}

printAlunos(alunos)