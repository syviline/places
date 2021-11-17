String.prototype.format = function () { // форматирует строку. "dsf {0} fds".format('asd') = "dsf asd fds"
    var args = arguments;
    return this.replace(/{(\d+)}/g, function (match, number) {
        return typeof args[number] != 'undefined'
            ? args[number]
            : match
            ;
    });
};


let search = ''
let page = 1

let xhr = new XMLHttpRequest()
let memoryPlaces = document.querySelector('.memory-places')

function appendElements(response) {
    response = JSON.parse(response)
    memoryPlaces.innerHTML += templates.add_place
    response.forEach(el => {
        memoryPlaces.innerHTML += templates.place.format(el.id, el.photo, el.name, el.description)
    })
}

function updatePlaces() {
    xhr.open('GET', url + 'get_places?page=' + page.toString() + '&search=' + search)
    memoryPlaces.innerHTML = ''
    xhr.send()
    xhr.onload = () => {
        appendElements(xhr.response)
    }
}

updatePlaces()