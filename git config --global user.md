git config --global user.email "30816862+Harris-Logic@users.noreply.github.com"
git config --global user.name "Harris-Logic"

m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ git remote -v
origin  https://github.com/Harris-Logic/py-exp-llm-mcp-rag.git (fetch)
origin  https://github.com/Harris-Logic/py-exp-llm-mcp-rag.git (push)
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ ping -c 3 github.com
PING github.com (198.18.0.197) 56(84) bytes of data.
64 bytes from 198.18.0.197: icmp_seq=1 ttl=62 time=0.672 ms
64 bytes from 198.18.0.197: icmp_seq=2 ttl=62 time=1.83 ms
64 bytes from 198.18.0.197: icmp_seq=3 ttl=62 time=1.05 ms

--- github.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 0.672/1.182/1.825/0.480 ms
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ git config --list | grep -E "(proxy|http|https)"
remote.origin.url=https://github.com/Harris-Logic/py-exp-llm-mcp-rag.git
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ git config --global http.sslVerify false && git pull --tags origin main
From https://github.com/Harris-Logic/py-exp-llm-mcp-rag
 * branch            main       -> FETCH_HEAD
Already up to date.
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ git config --global http.sslVerify true
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ ls -la ~/.ssh/
total 20
drwx------  2 m m 4096 10月  6 11:27 .
drwxr-x--- 30 m m 4096 10月 16 00:05 ..
-rw-------  1 m m  103 10月  5 22:54 authorized_keys
-rw-------  1 m m  978 10月  6 11:27 known_hosts
-rw-r--r--  1 m m  142 10月  6 11:27 known_hosts.old
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ ssh -T git@github.com
Connection closed by 198.18.0.197 port 22
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ ssh-keygen -t rsa -b 4096 -C "m@m-Virtual-Machine" -f ~/.ssh/id_rsa -N ""
Generating public/private rsa key pair.
Your identification has been saved in /home/m/.ssh/id_rsa
Your public key has been saved in /home/m/.ssh/id_rsa.pub
The key fingerprint is:
SHA256:U6qyJaDRvhyTODF8Uo6H4TzEHJWbrmR/Cy+JwDZn5sA m@m-Virtual-Machine
The key's randomart image is:
+---[RSA 4096]----+
| ....            |
|o ..             |
| = .o     .      |
|=.*o     o       |
|*O++    S        |
|.E=B   . .       |
|O /.+ o          |
| = Oo*           |
|  o +o.          |
+----[SHA256]-----+
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ cat ~/.ssh/id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC14mE9lyuwjti1i0sc88QQr+iZg2tu68kGHGEH4aGmndjKByhfyakBd3FZ/kxItn77NCCX2HObhaw7MDPnb8dG4jemcZxduSSWS0cJVkm3z/looNdxLOAEk4xF/7oqJLY0nIX3koAKajpIg+B/uMF1YPf+uGMsT8P1lbqI6KGvpyLZ5ZYJBfwYQ/TC87yAYxj1WfeM+MYYqnQeXnU4Vp49W+okDZcTwfbauGzhRYO8UwChCxezNrCp8OdDvMLdPx0mHcjYexHN9bGL+Z1KnUEQ0ntW1R/4owuJaEl16T0aC+ChujtSWHs4ks3isRQR1CU5s6PG6g084jQ5GiSdjzEJ1vOk6sVx+pD1wOt4UISp8fccfpUUJ+DcAJOhM09rF4jGbk/juXOOTHEDvirxq4WB1PqXXcy1CGMPiy8ShTAArDcc5WN4V37J/4gDuElSuncEhzX8sarvKeWujlJsufHyMf0bGzSrugxb5I8uIyc6J7Ls4QzN2nHAzO27GYs+OGEiLdtcqlWuJA1qYVUtoE4q6guA9g7k+iUTAxW9eUA0obYBRYcThxchNu0qsrJs34rzH0QGuKgzJHfuvlcRuvZdzLqLGyxj7ddARaYttxwJh4eSnCi8eRyLizOmsfZdkq9ngi5+R3Li3bWp8NInKcQwO8wki3/ujfaDmRSubu1OsQ== m@m-Virtual-Machine
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ ssh -T git@github.com
Connection closed by 198.18.0.197 port 22
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ ssh -T git@github.com
Connection closed by 198.18.1.16 port 22
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ git remote set-url origin git@github.com:Harris-Logic/py-exp-llm-mcp-rag.git
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ ssh -T git@github.com
Connection closed by 198.18.1.16 port 22


m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ git remote -v
origin  git@github.com:Harris-Logic/py-exp-llm-mcp-rag.git (fetch)
origin  git@github.com:Harris-Logic/py-exp-llm-mcp-rag.git (push)
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ git remote set-url origin https://github.com:Harris-Logic/py-exp-llm-mcp-rag.git
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ git remote -v
origin  https://github.com:Harris-Logic/py-exp-llm-mcp-rag.git (fetch)
origin  https://github.com:Harris-Logic/py-exp-llm-mcp-rag.git (push)
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ git remote set-url origin https://github.com/Harris-Logic/py-exp-llm-mcp-rag.git
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ git remote -v
origin  https://github.com/Harris-Logic/py-exp-llm-mcp-rag.git (fetch)
origin  https://github.com/Harris-Logic/py-exp-llm-mcp-rag.git (push)
m@m-Virtual-Machine:~/py-exp-llm-mcp-rag$ 