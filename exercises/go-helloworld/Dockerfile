FROM golang:alpine

LABEL maintainer="Sergei Ulianov"

WORKDIR /go/src/app

COPY . /go/src/app

RUN go mod init helloworld

RUN  go build  -o helloworld

EXPOSE 6111

CMD ["./helloworld"]

