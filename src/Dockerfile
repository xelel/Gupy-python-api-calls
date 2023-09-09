FROM python:3.10
LABEL maintainer = "Gupy"

ENV server_address=''
ENV database_name=''  
ENV db_username=''     
ENV password=''    
ENV gupy_token=''
COPY ./requirements.txt ./

ADD odbcinst.ini /etc/odbcinst.ini

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && wget http://archive.ubuntu.com/ubuntu/pool/main/g/glibc/multiarch-support_2.27-3ubuntu1.5_amd64.deb \
    && apt-get install ./multiarch-support_2.27-3ubuntu1.5_amd64.deb \
    && apt-get install -y build-essential cmake \
    && ACCEPT_EULA=Y apt-get install msodbcsql17 unixodbc-dev -y

RUN wget https://dev.mysql.com/get/Downloads/Connector-ODBC/8.0/mysql-connector-odbc-8.0.29-linux-glibc2.12-x86-64bit.tar.gz
RUN tar xvf mysql-connector-odbc-8.0.29-linux-glibc2.12-x86-64bit.tar.gz
RUN cp -r /mysql-connector-odbc-8.0.29-linux-glibc2.12-x86-64bit/bin/* /usr/local/bin/
RUN cp -r /mysql-connector-odbc-8.0.29-linux-glibc2.12-x86-64bit/lib/* /usr/local/lib/
RUN chmod 777 /usr/local/lib/libmy*
RUN apt-get install libodbc1 -y
RUN apt-get install odbcinst1debian2 -y
RUN myodbc-installer -a -d -n "MySQL ODBC 8.0 Driver" -t "Driver=/usr/local/lib/libmyodbc8w.so"
RUN myodbc-installer -a -d -n "MySQL ODBC 8.0" -t "Driver=/usr/local/lib/libmyodbc8a.so"

RUN pip3 install --upgrade pip
RUN pip3 --no-cache-dir install -r requirements.txt

WORKDIR /
COPY ./ /
EXPOSE 9000
CMD ["python3", "-u", "-m", "main"]
