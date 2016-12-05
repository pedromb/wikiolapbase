# WikiOlapBase (WOB)

O WikiOlapBase é uma aplicação web escrita em Python (Django) que visa integrar dados abertos 
e disponibilizá-los através de uma API REST. Este projeto surgiu como Trabalho de Conclusão de 
Curso do aluno Pedro Magalhães Bernardo no curso de Engenharia de Computação no CEFET-MG. 
O projeto ainda está em desenvolvimento e por isso possui diversas melhorias em aberto.

##Infraestrutura

A aplicação utiliza o Cassandra, Mongo e Spark.
Para tornar o desenvolvimento mais simples e abstrair as dependências utilizamos 3 containers 
do Docker. O primeiro container executa um servidor do Cassandra, o segundo um servidor do 
Mongo e o terceiro o servidor Spark e a aplicação Django. A utilização do Docker nesse contexto
é apenas para desenvolvimento, essa configuração não é própria para produção.  Siga os passos
abaixos para iniciar o desenvolvimento.

##1.Cassandra

Caso você não possua a imagem o Docker irá realizar o download direto do Docker Hub.
Para saber mais sobre essa imagem acesse https://hub.docker.com/_/cassandra/

```docker run --name wikiolapbase-cassandra -d cassandra:3.0```

##2.Mongo

Caso você não possua a imagem o Docker irá realizar o download direto do Docker Hub.
Para saber mais sobre essa imagem acesse https://hub.docker.com/_/mongo/

```docker run --name wikiolapbase-mongo -d mongo:3.2.9```

##3.Spark+Aplicação

Dentro do diretório onde você clonou este repositório execute o comando abaixo para
criar a imagem do container que possui a aplicação. Esse processo pode demorar alguns minutos.


```docker build -t wikiolapbase-app:latest . ```


Após construída a imagem, você deve iniciar o container e fazer o link com os servidores do
Cassandra e do Mongo que você iniciou anteriormente. Para isso execute o comando abaixo.

```docker run -it -p 8000:8000 --name wikiolapbase --link wikiolapbase-cassandra:cassandra --link wikiolapbase-mongo:mongo -d wikiolapbase-app```

Após feito isso você conseguirá acessar a aplicação em localhost:8000. Note que pode demorar
alguns minutos até a aplicação ficar disponível, isso acontece devido ao tempo necessário
para o cluster do Spark inicializar. 


##4.Debug

Se você seguir esses passos você conseguirá executar a aplicação, mas não realizar debug,
caso deseje executar a aplicação e observar os outputs da mesma como se estivesse executando
localmente. Faça o seguinte:

    1.Antes de criar a imagem do container da aplicação no passo 3, delete a 
    linha 70 do arquivo Dockerfile que acompanha esse repositório.
    
    2.Repita os passos do passo 3 (criar imagem e iniciar o container).

    3.Feito isso, a aplicação não será iniciada manualmente, você pode então acessar a linha
    de comando do seu container, que possui a aplicação, e executá-la diretamente por la. 
    Para isso execute o comando:

    ```docker exec -it id_do_seu_container bash```

    Para encontrar o id do seu container execute o comando:

    ```docker ps```

    4.Com isso você terá acesso ao bash e poderá executar a aplicação diretamente por la.
    Para isso execute os comandos:

    ```$SPARK_HOME/sbin/start-master.sh
    $SPARK_HOME/sbin/start-slave.sh "spark://$HOSTNAME:7077"
    python3 wikiolapbase/manage.py sync_cassandra
    python3 /wikiolapbase/manage.py runserver 0.0.0.0:8000
    ```

    Os 2 primeiros comandos iniciam o cluster do Spark, o segundo sincroniza o servidor do Cassandra
    com a aplicação. O último comando inicia a aplicação, assim você consegue observar os outputs como se
    estivesse executando a aplicação localmente. Mais uma vez, você poderá acessar a aplicação em localhost:8000

##Executando localmente

Caso você deseje executar a aplicação localmente, e não utilizar os containers do Docker
você terá que fazer a instalação manual do Cassandra e do Mongo. O restante das dependências
você pode utilizar o arquivo Dockerfile que acompanha esse repositório como base. No entanto,
indico fortemente a utilização dos containers Docker como explicado nesse documento.

##Contato

Se deseja contribuir ou possui alguma dúvida entre em contato.
