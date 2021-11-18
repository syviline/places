String.prototype.format = function () { // форматирует строку. "dsf {0} fds".format('asd') = "dsf asd fds"
    var args = arguments;
    return this.replace(/{(\d+)}/g, function (match, number) {
        return typeof args[number] != 'undefined'
            ? args[number]
            : match
            ;
    });
};


let templates = {add_place: '<div class="object"><a href="/add_place"><div class="add_place"><img src="/static/icons/add.svg" alt=""><span>Добавить место</span></div></a></div>',
    place: '<div class="object"><a href="/place/{0}"><img src="{1}" alt="" class="img"><h2>{2}</h2><h5>{3}</h5></a></div>',
    add_serie: '<div class="object"><a href="/add_serie"><div class="add_place"><img src="/static/icons/add.svg" alt=""><span>Добавить серию</span></div></a></div>',
    serie: '<div class="object"><a href="/serie/{0}"><img src="{1}" alt="" class="img"><h2>{2}</h2><h5>{3}</h5></a></div>',
    pageElementPlaces: '<button class="page-item" id="page-item-{0}" onclick="changePagePlaces({0})">{0}</button>',
    pageElementPlacesChosen: '<button class="page-item chosen" id="page-item-{0}" onclick="changePagePlaces({0})">{0}</button>',
    pageElementSeries: '<button class="page-item" id="page-item-{0}" onclick="changePageSeries({0})">{0}</button>',
    pageElementSeriesChosen: '<button class="page-item chosen" id="page-item-{0}" onclick="changePageSeries({0})">{0}</button>',
    nothingFound: '<div>Ничего не найдено...</div>',
    placeInSerie: '<img src="{0}" alt="" class="viewplace_image"><div class="serie-place-flex"><div class="place-description"><h6 class="place_label" style="margin-top: 20px;">ОПИСАНИЕ МЕСТА</h6><div class="place_info">{1}</div></div><div class="place-info" style="text-align: right"><h6 class="place_label" style="margin-top: 20px;">ШИРОТА</h6><div class="latitude">{2}</div><h6 class="place_label" style="margin-top: 20px;">ДОЛГОТА</h6><div class="longitude">{3}</div></div></div>'
}

let url = 'http://127.0.0.1:8000/'