let search = ''
let pagePlaces = 1
let pageSeries = 1
let currentPagesAmountPlaces = 1
let currentPagesAmountSeries = 1

let memoryPlaces = document.querySelector('.memory-places')
let series = document.querySelector('.series')

function appendElementsPlaces(response) {
    if (search == '')
        memoryPlaces.innerHTML += templates.add_place
    response.forEach(el => {
        memoryPlaces.innerHTML += templates.place.format(el.id, el.photo, el.name, el.description)
    })
    if (response.length === 0 && search != '') {
        memoryPlaces.innerHTML += templates.nothingFound
    }
}

function appendElementsSeries(response) {
    if (search == '')
        series.innerHTML += templates.add_serie
    response.forEach(el => {
        series.innerHTML += templates.serie.format(el.id, el.photo, el.name, el.description)
    })
    if (response.length === 0 && search != '') {
        series.innerHTML += templates.nothingFound
    }
}

function searchFunc() {
    search = document.querySelector('#searchbar').value
    pagePlaces = 1
    pageSeries = 1
    updatePlaces()
    updateSeries()
}

function updatePlaces() {
    let xhr = new XMLHttpRequest()
    xhr.open('GET', url + 'get_places?page=' + pagePlaces.toString() + '&search=' + search.toLowerCase())
    xhr.send()
    xhr.onload = () => {
        let resp = JSON.parse(xhr.response)
        console.log(resp)
        currentPagesAmountPlaces = resp.pagesAmount
        memoryPlaces.innerHTML = ''
        appendElementsPlaces(resp.places)
        updatePageListPlaces()
    }
}

function updateSeries() {
    let xhr = new XMLHttpRequest()
    xhr.open('GET', url + 'get_series?page=' + pageSeries.toString() + '&search=' + search.toLowerCase())
    xhr.send()
    xhr.onload = () => {
        let resp = JSON.parse(xhr.response)
        currentPagesAmountSeries = resp.pagesAmount
        series.innerHTML = ''
        appendElementsSeries(resp.series)
        updatePageListSeries()
    }
}

function updatePageListPlaces() {
    let memoryPageList = document.querySelector('.memory-places-pages')
    memoryPageList.innerHTML = ''
    if (currentPagesAmountPlaces > 1) {
        for (i = 1; i <= currentPagesAmountPlaces; i++) {
            if (pagePlaces == i)
                memoryPageList.innerHTML += templates.pageElementPlacesChosen.format(i)
            else
                memoryPageList.innerHTML += templates.pageElementPlaces.format(i)
        }
    }
}

function updatePageListSeries() {
    let seriesPageList = document.querySelector('.series-pages')
    seriesPageList.innerHTML = ''
    if (currentPagesAmountSeries > 1) {
        for (i = 1; i <= currentPagesAmountSeries; i++) {
            if (pageSeries == i)
                seriesPageList.innerHTML += templates.pageElementSeriesChosen.format(i)
            else
                seriesPageList.innerHTML += templates.pageElementSeries.format(i)
        }
    }
}

function changePagePlaces(page) {
    pagePlaces = page
    updatePlaces()
    document.querySelector("#memory-places-h1").scrollIntoView()
}

function changePageSeries(page) {
    pageSeries = page
    updateSeries()
    document.querySelector("#series-h1").scrollIntoView()
}

updatePlaces()
updateSeries()