const cursos = data
const marke = document.getElementById('favoritos')
let lista = JSON.parse(localStorage.getItem('fixados')) || []

async function start(){
    lista = await fixadosBD('[]');
}

async function fixadosBD(lista) {
   
    try {
        lista = lista.toString()
        if(lista==''){lista='[]'}
        
        const res = await fetch(`/fixados/${lista}`, { method: 'POST' });
        resultado = await res.json();
        console.log(resultado)

    } catch (error) {
        console.error('Erro:', error);
    }
    return JSON.parse(resultado)
}

function marker(id) {
    const curso = cursos.find(u => u[0] === id);
    if (!lista.some(item => item[0] === id)) {
        lista.push(curso)
    }
    printar()
}
function delmarker(id) {
    const curso = cursos.find(u => u[0] === id);
    lista = lista.filter(e => e[0] !== curso[0])
    document.getElementById(`item-id-${id}`).style.display = 'block'
    document.getElementById(`checkbox-id-${id}`).checked = false;
    printar()
}

async function printar() {
    marke.innerHTML = ''
    //let data = await fixadosBD(lista)
    
    localStorage.setItem('fixados',JSON.stringify(lista))
    lista = JSON.parse(localStorage.getItem('fixados'))
    if(lista.length){
    lista = lista.map(e=>{
        if (cursos.some(item => item[0] === e[0])){
            return cursos.find(u => u[0] === e[0])
        }
    })
    }
    console.log(lista)


    lista.forEach(e => {
        marke.innerHTML += `
            <a href="/registros/${e[0]}">
                <div class="item">
                    <div class="head-item">
                        <h3 style="flex: 3;">${e[1]}</h3>
                        <label class="container">
                            <input type="checkbox" class="checkbox" value="${e[0]}" checked/>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 75 100" class="pin">
                                <line stroke-width="12" stroke="black" y2="100" x2="37" y1="64" x1="37"></line>
                                <path stroke-width="10" stroke="black"
                                    d="M16.5 36V4.5H58.5V36V53.75V54.9752L59.1862 55.9903L66.9674 67.5H8.03256L15.8138 55.9903L16.5 54.9752V53.75V36Z">
                                </path>
                            </svg>
                        </label>
                    </div>
                    <div class="main-item">
                        <div style="flex: 3;">
                            <p>${e[3][0] != 0 ? 'em espera ➤ ' + e[3][0] : ''}</p>
                            <p>${e[3][1] != 0 ? 'confirmado ➤ ' + e[3][1] : ''}</p>
                            <p>${e[3][2] != 0 ? 'pendente ➤ ' + e[3][2] : ''}</p>
                            <p>${e[3][3] != 0 ? 'negado ➤ ' + e[3][3] : ''}</p>
                            <p>${e[3][4] != 0 ? 'em espera do responsável ➤ ' + e[3][4] : ''}</p>
                        </div>
                        <div class="notification">
                            <div style="display: flex;">
                                ${e[2] > 0 ?
                `<img src="../static/img/notifications.svg" width="30px" alt="notification">
                                <p>${e[2]}</p>`
                : ''}

                            </div>
                        </div>
                    </div>
                </div>
            </a>
                `
        document.getElementById(`item-id-${e[0]}`).style.display = 'none'
    })

    if (lista.length) {
        document.querySelectorAll('.none').forEach(e => e.style.display = 'none')
    } else {
        document.querySelectorAll('.none').forEach(e => e.style.display = 'flex')
    }
    addevento()
}
function addevento() {
    let checkbox = document.querySelectorAll('.checkbox')
    checkbox.forEach(e => {
        e.replaceWith(e.cloneNode(true));
    });
    checkbox = document.querySelectorAll('.checkbox')
    checkbox.forEach(e => e.addEventListener('click', () => {
        if (e.checked) {
            marker(parseInt(e.value))
        } else {
            delmarker(parseInt(e.value))
        }
    }))
}


printar()