async function customStartIntro() {
  $('#scroll-blocker').addClass('stop-scrolling')
  var intro = introJs();
  intro.setOption('tooltipClass', 'customDefault') //custom buttons and general layout of tooltip
  intro.setOptions({
    steps: [
      {
        element: '#year-slider',
        intro: "<b>Oś czasu</b><hr> \
              <img width='54px' height='50px' src='assets/Images/map_image.PNG' style='float: right;'> \
              <p style='text-align: left;'>Zmieniając położenie slidera można obejrzeć stan interaktywnej mapy Polski w wybranym roku.</p><hr> \
              <img src='assets/Images/plate_image.PNG' style='float: right;'> \
              <p style='text-align: left;'>Kliknięcie kolorowej tabliczki spowoduje podświetlenie korespondującego zdarzenia na poniższym wykresie.</p>",
        position: 'right'
      },
      {
        element: '#map-filters',
        intro: "<b>Filtr danych</b><hr> \
              <div><input type='checkbox' id='ac' value disabled><label for='ac'>Liczba aktywnych firm</label></div> \
              Wyświetla na poniższej mapie informację o liczbie \
              aktywnych działalności gospodarczych w danym województwie.<hr> \
              <div><input type='checkbox' id='percent' value disabled><label for='percent'>% zamkniętych firm</label></div> \
              Wyświetla odsetek działalności upadłych w danym województwie, do roku zaznaczonego na osi czasu.",
        position: 'right'
      },
      {
        element: '#map',
        intro: '<style> \
              body {font-family: Arial;}\
              .tab { \
                overflow: hidden;\
                border: 1px solid #ccc;\
                background-color: #f1f1f1;\
              }\
              .tab button {\
                background-color: inherit;\
                float: left;\
                border: none;\
                outline: none;\
                cursor: pointer;\
                padding: 14px 16px;\
                transition: 0.3s;\
                font-size: 17px;\
              }\
              .tab button:hover {\
                background-color: #ddd;\
              }\
              .tab button.active {\
                background-color: #ccc;\
              }\
              .tabcontent {\
                display: none;\
                padding: 6px 12px;\
                border: 1px solid #ccc;\
                border-top: none;\
              }\
              </style>\
              </head>\
              <body>\
              <h3>Mapa województw</h3>\
              <div class="tab">\
                <button style="display: block; width: 36%;" class="tablinks active" onclick="openTab(event,\'usage\')">Obsługa</button>\
                <button style="display: block; width: 28%;" class="tablinks" onclick="openTab(event,\'data\')">Opis</button>\
                <button style="display: block; width: 36%;" class="tablinks" onclick="openTab(event,\'features\')">Działanie</button>\
              </div>\
              <div id="usage" class="tabcontent" style="display: block;">\
                <p>Aby <b>zaznaczyć</b> interesujące nas województwo należy w nie kliknąć <u>lewym przyciskiem myszy</u>.</p><hr> \
                <p>Klikając z <u>shiftem</u> można zaznaczyć kilka województw jednocześnie.</p><hr> \
                <p>Aby <b>wyłączyć zaznaczenie</b> należy ponownie kliknąć w zaznaczone województwo <u>lewym przyciskiem myszy</u>.<br> \
                Jeżeli zaznaczone było więcej niż jedno województwo, należy kliknąć dwukrotnie.</p><hr> \
                <p>Mapę można <b>przybliżać i oddalać</b> korzystając z przycisków <u>Zoom in</u> i <u>Zoom out</u> w prawym górnym rogu.</p> \
              </div>\
              <div id="data" class="tabcontent">\
                <p>Kartogram przedstawia liczbę aktywnych firm lub odsetek upadłych (w zależności od wybranej powyżej opcji), w podziale na województwa. \
                Dane aktualizują się, przedstawiając zawsze stan z roku wybranego na osi czasu.</p>\
              </div>\
              <div id="features" class="tabcontent">\
                <p>Kliknięcie na mapie spowoduje, że dane przedstawione na wykresie umieralności firm (po prawo) \
                oraz przeciętnego czasu życia ze względu na sekcję PKD (poniżej), zaktualizują się i będą dotyczyć \
                tylko wybranych województw. Brak zaznaczenia jest równoważny zaznaczeniu wszystkich województw, czyli całej Polski.</p> \
              </div>',
            position: 'right'
          },
          {
            element: '#timeline',
            intro: "<b>Wykres umieralności firm</b> \
              <p>Wykres przedstawia liczbę firm, które upadły w danym miesiącu.</p> <hr>\
              <p>Dane można filtrować wybierając interesujące nas województwa i/lub sekcję PKD.</p><hr> \
              Po <b>najechaniu</b> na któryś z zaznaczonych punktów pojawia się szczegółowy opis tego zdarzenia.",
            position: 'left',
            scrollTo: 'pkd-tree'
          },
          {
            element: '#pkd-tree',
            intro: '<style> \
            body {font-family: Arial;}\
            .tab { \
              overflow: hidden;\
              border: 1px solid #ccc;\
              background-color: #f1f1f1;\
            }\
            .tab button {\
              background-color: inherit;\
              float: left;\
              border: none;\
              outline: none;\
              cursor: pointer;\
              padding: 14px 16px;\
              transition: 0.3s;\
              font-size: 17px;\
            }\
            .tab button:hover {\
              background-color: #ddd;\
            }\
            .tab button.active {\
              background-color: #ccc;\
            }\
            .tabcontent {\
              display: none;\
              padding: 6px 12px;\
              border: 1px solid #ccc;\
              border-top: none;\
            }\
            </style>\
            </head>\
            <body>\
            <h3>Mapa PKD</h3>\
            <div class="tab">\
              <button style="display: block; width: 36%;" class="tablinks active" onclick="openTab(event,\'usage\')">Obsługa</button>\
              <button style="display: block; width: 28%;" class="tablinks" onclick="openTab(event,\'data\')">Opis</button>\
              <button style="display: block; width: 36%;" class="tablinks" onclick="openTab(event,\'features\')">Działanie</button>\
            </div>\
            <div id="usage" class="tabcontent" style="display: block;">\
              <p>Aby <b>wybrać</b> interesującą nas sekcję lub dywizję PKD należy w nią kliknąć <u>lewym przyciskiem myszy</u>.</p><hr> \
              <p>Ponowne kliknięcie spowoduje odznaczenie i powrót do bardziej ogólnego widoku.</p><hr> \
              <p>Po najechaniu myszką na obszar pojawia się nazwa sekcji/dywizji oraz konkretne dane liczbowe.</p> \
            </div>\
            <div id="data" class="tabcontent"> \
              <p>Kolorem pokazany jest średni czas życia działalności w danej sekcji PKD.</p><hr> \
              <p>Pole prostokąta oddaje ilość powstałych w danej sekcji firm.</p><hr> \
              <p><b>Klikając</b> w daną sekcję można wyświetlić szczegółowe informacje o jej dywizjach.</p> \
              </div>\
            <div id="features" class="tabcontent">\
              <p>Zaznaczenie sekcji/dywizji spowoduje, że na powyższym wykresie umieralności firm zostaną wyświetlone tylko dane \
              dotyczące wybranej sekcji/dywizji.</p><hr> \
              <p>Brak zaznaczenia jest równoważny zaznaczeniu wszystkich sekcji i dywizji jednocześnie.</p>\
            </div>',
        position: 'top'
      },
      {
        element: '#prediction-input',
        intro: '<b>Predykcja - wprowadzanie danych</b><br> \
              Wypełnij pola by sprawdzić ile przetrwa Twój biznes!',
        position: 'bottom'
      },
      {
        element: '#pred-output',
        intro: '<b>Predykcja - wyniki</b><br> \
              <p>Prognozy co do przetrwania Twojej firmy znajdują się poniżej.</p><hr> \
              <p>Wykres przedstawia prawdopodobieństwo upadku Twojej działalności w kolejnych latach.</p>',
        position: 'bottom'
      }
    ]
  });
  intro.onbeforechange(function (targetElement) {
    switch (targetElement.id) {
      case "year-slider":
        $('#main').find("#map-section").prependTo('#main');
        break;
      case "pkd-tree":
        $('#main').find("#map-section").prependTo('#main');
        $('.introjs-arrow').attr('style', 'opacity: 0 !important;');
        break;
      case "prediction-input":
        $('#main').find("#prediction-section").prependTo('#main');
        $('.introjs-arrow').attr('style', 'opacity: 0 !important;');
        break;
      case "pred-output":
        $('#main').find("#prediction-section").prependTo('#main');
        $('.introjs-arrow').attr('style', 'opacity: 0 !important;');
        break;
      default:
        $('.introjs-arrow').css({ opacity: 1 });
    }
  });
  intro.onexit(function () {
    $('#main').find("#prediction-section").prependTo('#main');
    $('#main').find("#map-section").prependTo('#main');
    $('#main').find("#title-section").prependTo('#main');
  })
  intro.start();
  await new Promise(r => setTimeout(r, 1000));
  intro.nextStep().previousStep();
}

function openTab(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}
