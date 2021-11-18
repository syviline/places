currentPlaceIndex = 0

function updateCounter() {
    document.querySelector('#serieCounter').innerHTML = (currentPlaceIndex + 1).toString() + '/' + places.length.toString()
}

function placeNext() {
    if (currentPlaceIndex >= places.length - 1)
        return
    if (currentPlaceIndex === places.length - 2) {
        document.querySelector('.arrow-forward').classList.add('inactive')
    }
    document.querySelector('.arrow-back').classList.remove('inactive')
    currentPlaceIndex++
    renderPlace()
}

function placeBack() {
    if (currentPlaceIndex === 0) {
        return
    }
    if (currentPlaceIndex === 1) {
        document.querySelector('.arrow-back').classList.add('inactive')
    }
    document.querySelector('.arrow-forward').classList.remove('inactive')
    currentPlaceIndex--
    renderPlace()
}

function renderPlace() {
    updateCounter()
    let placeobj = document.querySelector('.serie-place-info')
    placeobj.innerHTML = templates.placeInSerie.format(places[currentPlaceIndex].photo, places[currentPlaceIndex].description, places[currentPlaceIndex].latitude, places[currentPlaceIndex].longitude)
    document.querySelector('.serie-place-name').innerHTML = '<a href="/place/{0}" class="header_a">{1}</a>'.format(places[currentPlaceIndex].id, places[currentPlaceIndex].name)
}

function deleteFromSerie() {
    if (confirm('Вы уверены что хотите удалить это место из серии?')) {
        let xhr = new XMLHttpRequest()
        xhr.open('GET', url + 'remove_from_serie/' + serieid + '/' + places[currentPlaceIndex].id)
        xhr.send()
        xhr.onload = () => {
            places.splice(currentPlaceIndex, 1)
            if (currentPlaceIndex != 0)
                currentPlaceIndex--
            renderPlace()
        }
    }
}

renderPlace()