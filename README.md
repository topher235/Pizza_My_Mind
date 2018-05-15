# Pizza_My_Mind

Website for the Pizza My Mind event hosted by the Physics, Computer Science, and Engineering department at CNU.

Steps for resetting server with the current git repo in case it resets again:
1. Login to server
2. Login to root with "sudo su -"
3. Navigate to ~/opt/pmm
4. If no local git repo:
  a. init local repo and add .
  b. config user.name and user.email
  c. remote add origin this url
5. If local git repo:
  a. check config for user.name and user.email
  b. check remote url
6. fetch --all
7. reset --hard origin/master
