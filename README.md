# S3_AJAX_API
Students

```bash
curl http://127.0.0.1:5000/students
```

```bash
curl -X POST -H 'Content-Type:application/json' -d '{"name":"Gift Chimphonda", "interests":["1", "2"]}' http://127.0.0.1:5000/students
```

Interests
```bash
curl http://127.0.0.1:5000/interests
```
```bash
curl http://127.0.0.1:5000/interests/1
```
```bash
curl -X POST -H 'Content-Type:application/json' -d '{"name":"Scrabble"}' http://127.0.0.1:5000/interests
```
```bash
curl -X PATCH -H 'Content-Type:application/json' -d '{"name":"Bawo"}' http://127.0.0.1:5000/interests/2
```
```bash
curl -X DELETE http://127.0.0.1:5000/interests/3
```
