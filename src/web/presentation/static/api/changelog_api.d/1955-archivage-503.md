---
type: modifie
date: 2026-10-14
pr: 1955
---

`POST /api/v1/offres/archiver` : si l'offre ne peut pas être retirée de l'index de
recherche, la requête renvoie désormais `503 Service Unavailable` et l'offre n'est
pas archivée. Auparavant, l'offre était archivée et la requête renvoyait `200`
alors que l'offre restait dans l'index. La requête peut être renvoyée plus tard.
