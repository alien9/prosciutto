ssh alien9.net -t "sudo chown -R tiago.tiago works/prosciutto/database"
rsync -rCv ../prosciutto alien9.net:works/
scp config.production.py alien9.net:works/prosciutto/config.py
ssh alien9.net -t "sudo chown -R www-data:www-data works/prosciutto/database"
