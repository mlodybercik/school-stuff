Do zrobienia trzy aplikacje opierające się na brokerze MQTT

### Aplikacja 1
Generator wysyłający do brokera MQTT jakąś informację. Zajętość dysków, albo zużycie CPU/RAM. Informacje są wysyłane ze znacznikiem czasu.

### Aplikacja 2
Aplikacja nasłuchująca brokera a następnie te informacje wysyła za pomocą POST na aplikacje nr3.

### Aplikacja 3
Serwer HTTP nasłuchujący na ścieżce POST i GET.
POST - aplikacja 2 wrzuca na serwer ostatnie informacje
GET  _ użytkownik może ściągnąć dane informacje za pomocą REST'a.