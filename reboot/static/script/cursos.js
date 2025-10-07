const cursos = data
const marke = document.getElementById('favoritos')
const lista = []

function addmarker(id) {
    let idCursos = cursos.map(e=>e[0])
    id = idCursos.indexOf(parseInt(id))

    if(!lista.includes(cursos[id])){
        lista.push(cursos[id])
    }
    printar()
}

function delmarker(id) {
    let id_lista = lista.map(e => e[0])
    let id_del = id_lista.indexOf(id)
    lista.splice(id_del, 1)
    document.getElementById(`${id}`).style.display = 'flex'
    printar()
}

const notalert = document.querySelectorAll('.none')
function printar() {
    marke.innerHTML = ''

    if(lista.length){
        notalert.forEach(e=>e.style.display = 'none')
    }else{
        notalert.forEach(e=>e.style.display = 'flex')
    }

    lista.forEach(e => {
        marke.innerHTML += `
            <li>
                <a href="/registros/${e[0]}">
                    <div style="flex: 3;">${e[1]}</div>
                    <div class="notification">
                        ${e[2]>0?
                            `
                            <img src="../static/img/notifications.svg" width="40px" alt="notification">
                            <p>${e[2]}</p>
                            `
                            :
                            ''
                        }
                    </div>
                </a>
                <button id="keep2" onclick="delmarker(${e[0]})">
                    <img src="../static/img/keep.svg" width="40px" alt="notification">
                </button>
            </li>
                `
        document.getElementById(`${e[0]}`).style.display = 'none'
    })
}

printar()